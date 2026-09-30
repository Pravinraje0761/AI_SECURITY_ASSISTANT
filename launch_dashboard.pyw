"""One-click launcher for AI Digital Bodyguard.

Shows an animated splash screen while it starts the backend, signs in with
the demo account, seeds demo data, then fades the dashboard in.
Runs without a console window (.pyw). Double-click this file or
"Launch Dashboard.bat".
"""
import math
import os
import subprocess
import sys
import time

import requests
from PyQt6.QtCore import (
    QEasingCurve, QEvent, QObject, QPointF, QPropertyAnimation, QRectF, Qt, QThread, QTimer,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QBrush, QColor, QConicalGradient, QFont, QLinearGradient, QPainter,
    QPainterPath, QPen, QRadialGradient,
)
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QWidget

BASE = os.path.dirname(os.path.abspath(__file__))
DESKTOP_DIR = os.path.join(BASE, "desktop")
BACKEND_DIR = os.path.join(BASE, "backend")
BACKEND_URL = "http://127.0.0.1:8000"
BACKEND_TIMEOUT = 45

sys.path.insert(0, DESKTOP_DIR)
from main import (  # noqa: E402  (desktop/main.py)
    LoginDialog, MainWindow, create_icon, seed_demo_data, try_demo_login,
)
from services.api_client import api  # noqa: E402
from ui.styles import DARK_STYLE  # noqa: E402

BG = QColor("#1a1a2e")
PANEL = QColor("#16213e")
ACCENT = QColor("#e94560")
PURPLE = QColor("#533483")
BLUE = QColor("#0f3460")
TEXT = QColor("#e0e0e0")
MUTED = QColor("#a0a0a0")
OK = QColor("#44dd88")

STEPS = [
    "Starting backend server",
    "Loading AI detection models",
    "Signing in",
    "Preparing dashboard data",
]


def backend_healthy():
    try:
        return requests.get(f"{BACKEND_URL}/health", timeout=2).status_code == 200
    except Exception:
        return False


class StartupWorker(QThread):
    """Does the slow startup work off the UI thread so animations stay smooth."""
    step = pyqtSignal(int, str)        # step index, detail text
    progress = pyqtSignal(float)       # 0.0 - 1.0
    done = pyqtSignal(object)          # token or None
    failed = pyqtSignal(str)

    backend_proc = None

    def run(self):
        self.step.emit(0, "Checking for running server...")
        self.progress.emit(0.05)
        if not backend_healthy():
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            try:
                StartupWorker.backend_proc = subprocess.Popen(
                    [sys.executable, "-m", "uvicorn", "app.main:app",
                     "--host", "127.0.0.1", "--port", "8000"],
                    cwd=BACKEND_DIR,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=flags,
                )
            except Exception as e:
                self.failed.emit(f"Could not launch backend: {e}")
                return
            start = time.time()
            while not backend_healthy():
                elapsed = time.time() - start
                if StartupWorker.backend_proc.poll() is not None:
                    self.failed.emit("Backend process exited during startup.\n"
                                     "Check backend/app.log for details.")
                    return
                if elapsed > BACKEND_TIMEOUT:
                    self.failed.emit("Backend did not respond within "
                                     f"{BACKEND_TIMEOUT} seconds.")
                    return
                self.step.emit(0 if elapsed < 3 else 1, f"Waiting for server... {int(elapsed)}s")
                self.progress.emit(0.05 + 0.5 * min(elapsed / 12, 1.0))
                time.sleep(0.3)

        self.step.emit(1, "Models ready")
        self.progress.emit(0.6)

        self.step.emit(2, "Authenticating demo account...")
        token = try_demo_login()
        self.progress.emit(0.75)

        if token:
            api.set_token(token)
            self.step.emit(3, "Seeding scans and alerts...")
            seed_demo_data()
        self.progress.emit(1.0)
        self.step.emit(len(STEPS), "Ready")
        time.sleep(0.4)
        self.done.emit(token)


class AnimatedSplash(QWidget):
    """Frameless splash: radar sweep, pulsing shield, step checklist, progress bar."""
    W, H = 560, 380

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint
                            | Qt.WindowType.WindowStaysOnTopHint
                            | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.W, self.H)
        self.setWindowOpacity(0.0)

        self._t = 0.0
        self._progress_target = 0.0
        self._progress = 0.0
        self._step = 0
        self._detail = "Initializing..."
        self._error = None

        self._tick = QTimer(self)
        self._tick.timeout.connect(self._advance)
        self._tick.start(16)

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(screen.center().x() - self.W // 2, screen.center().y() - self.H // 2)

    # --- state setters -------------------------------------------------
    def set_step(self, idx, detail):
        self._step = max(self._step, idx)
        self._detail = detail

    def set_progress(self, p):
        self._progress_target = max(self._progress_target, p)

    def set_error(self, msg):
        self._error = msg
        self._detail = "Startup failed"

    # --- animation ------------------------------------------------------
    def _advance(self):
        self._t += 0.016
        # ease displayed progress toward target
        self._progress += (self._progress_target - self._progress) * 0.08
        self.update()

    def fade(self, start, end, ms, on_done=None):
        anim = QPropertyAnimation(self, b"windowOpacity", self)
        anim.setDuration(ms)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        if on_done:
            anim.finished.connect(on_done)
        anim.start()
        self._fade_anim = anim

    # --- painting -------------------------------------------------------
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # card background
        card = QRectF(8, 8, self.W - 16, self.H - 16)
        grad = QLinearGradient(card.topLeft(), card.bottomRight())
        grad.setColorAt(0, QColor("#1f1f3a"))
        grad.setColorAt(1, BG)
        p.setPen(QPen(QColor(233, 69, 96, 90), 1.5))
        p.setBrush(grad)
        p.drawRoundedRect(card, 18, 18)

        self._paint_radar(p, QPointF(150, 175), 95)
        self._paint_text(p)
        self._paint_progress(p)
        p.end()

    def _paint_radar(self, p, c, r):
        # rings
        p.setBrush(Qt.BrushStyle.NoBrush)
        for i in range(1, 4):
            p.setPen(QPen(QColor(83, 52, 131, 110), 1))
            p.drawEllipse(c, r * i / 3, r * i / 3)
        p.drawLine(QPointF(c.x() - r, c.y()), QPointF(c.x() + r, c.y()))
        p.drawLine(QPointF(c.x(), c.y() - r), QPointF(c.x(), c.y() + r))

        # rotating sweep
        angle = (self._t * 140) % 360
        sweep = QConicalGradient(c, -angle)
        sweep.setColorAt(0.0, QColor(233, 69, 96, 170))
        sweep.setColorAt(0.18, QColor(233, 69, 96, 0))
        sweep.setColorAt(1.0, QColor(233, 69, 96, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(sweep))
        p.drawEllipse(c, r, r)

        # blips that flash when the sweep passes
        for bx, by, ba in ((0.45, -0.30, 40), (-0.55, 0.20, 200), (0.20, 0.60, 290), (-0.25, -0.55, 120)):
            diff = (angle - ba) % 360
            alpha = max(0, 255 - diff * 2.2)
            if alpha > 0:
                p.setBrush(QColor(68, 221, 136, int(alpha)))
                p.drawEllipse(QPointF(c.x() + bx * r, c.y() + by * r), 4, 4)

        # expanding pulse ring
        pulse = (self._t * 0.8) % 1.0
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(233, 69, 96, int(160 * (1 - pulse))), 2))
        p.drawEllipse(c, 30 + pulse * (r - 30), 30 + pulse * (r - 30))

        # shield with breathing glow
        breathe = 0.5 + 0.5 * math.sin(self._t * 3)
        glow = QRadialGradient(c, 55)
        glow.setColorAt(0, QColor(233, 69, 96, int(70 + 60 * breathe)))
        glow.setColorAt(1, QColor(233, 69, 96, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(glow)
        p.drawEllipse(c, 55, 55)

        s = 30
        shield = QPainterPath()
        shield.moveTo(c.x(), c.y() - s)
        shield.cubicTo(c.x() + s * 0.6, c.y() - s * 0.75, c.x() + s * 0.9, c.y() - s * 0.8, c.x() + s * 0.9, c.y() - s * 0.8)
        shield.cubicTo(c.x() + s * 0.95, c.y() + s * 0.2, c.x() + s * 0.5, c.y() + s * 0.75, c.x(), c.y() + s)
        shield.cubicTo(c.x() - s * 0.5, c.y() + s * 0.75, c.x() - s * 0.95, c.y() + s * 0.2, c.x() - s * 0.9, c.y() - s * 0.8)
        shield.cubicTo(c.x() - s * 0.9, c.y() - s * 0.8, c.x() - s * 0.6, c.y() - s * 0.75, c.x(), c.y() - s)
        sg = QLinearGradient(c.x(), c.y() - s, c.x(), c.y() + s)
        sg.setColorAt(0, ACCENT)
        sg.setColorAt(1, PURPLE)
        p.setBrush(sg)
        p.setPen(QPen(QColor(255, 255, 255, 200), 1.5))
        p.drawPath(shield)

        # check mark / "B" in shield
        p.setPen(QColor("white"))
        p.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        p.drawText(QRectF(c.x() - s, c.y() - s, 2 * s, 2 * s), Qt.AlignmentFlag.AlignCenter, "B")

    def _paint_text(self, p):
        x = 275
        p.setPen(ACCENT)
        p.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        p.drawText(QRectF(x, 40, 270, 34), Qt.AlignmentFlag.AlignLeft, "AI Digital Bodyguard")
        p.setPen(MUTED)
        p.setFont(QFont("Segoe UI", 10))
        p.drawText(QRectF(x, 74, 270, 20), Qt.AlignmentFlag.AlignLeft, "Starting security systems")

        # step checklist
        y = 115
        p.setFont(QFont("Segoe UI", 10))
        for i, label in enumerate(STEPS):
            cy = y + i * 34 + 9
            if i < self._step:
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(OK)
                p.drawEllipse(QPointF(x + 9, cy), 8, 8)
                p.setPen(QPen(QColor("#1a1a2e"), 2.2))
                p.drawPolyline([QPointF(x + 5, cy), QPointF(x + 8, cy + 3), QPointF(x + 13, cy - 3)])
                p.setPen(TEXT)
            elif i == self._step and self._error is None:
                # spinning arc
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(QPen(BLUE, 2.2))
                p.drawEllipse(QPointF(x + 9, cy), 7, 7)
                p.setPen(QPen(ACCENT, 2.2, cap=Qt.PenCapStyle.RoundCap))
                start = int(-self._t * 360 * 16) % (360 * 16)
                p.drawArc(QRectF(x + 2, cy - 7, 14, 14), start, 100 * 16)
                p.setPen(QColor("white"))
            elif i == self._step:
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(QColor("#ff4444"))
                p.drawEllipse(QPointF(x + 9, cy), 8, 8)
                p.setPen(QColor("#ff8888"))
            else:
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.setPen(QPen(QColor(160, 160, 160, 80), 1.5))
                p.drawEllipse(QPointF(x + 9, cy), 7, 7)
                p.setPen(QColor(160, 160, 160, 120))
            p.drawText(QRectF(x + 28, cy - 10, 240, 20),
                       Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)

    def _paint_progress(self, p):
        bar = QRectF(40, self.H - 70, self.W - 80, 8)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(PANEL)
        p.drawRoundedRect(bar, 4, 4)

        fill = QRectF(bar.x(), bar.y(), bar.width() * self._progress, bar.height())
        g = QLinearGradient(fill.topLeft(), fill.topRight())
        g.setColorAt(0, PURPLE)
        g.setColorAt(1, ACCENT)
        p.setBrush(g)
        p.drawRoundedRect(fill, 4, 4)

        # shimmer moving across the filled part
        if fill.width() > 20 and self._error is None:
            sx = fill.x() + (self._t * 220) % fill.width()
            sh = QLinearGradient(sx - 30, 0, sx + 30, 0)
            sh.setColorAt(0, QColor(255, 255, 255, 0))
            sh.setColorAt(0.5, QColor(255, 255, 255, 110))
            sh.setColorAt(1, QColor(255, 255, 255, 0))
            p.setBrush(sh)
            p.drawRoundedRect(fill, 4, 4)

        p.setFont(QFont("Segoe UI", 9))
        p.setPen(QColor("#ff8888") if self._error else MUTED)
        dots = "." * (int(self._t * 3) % 4) if self._error is None and self._step < len(STEPS) else ""
        p.drawText(QRectF(bar.x(), bar.y() + 14, bar.width() - 50, 20),
                   Qt.AlignmentFlag.AlignLeft, self._detail.rstrip(".") + dots)
        p.drawText(QRectF(bar.x(), bar.y() + 14, bar.width(), 20),
                   Qt.AlignmentFlag.AlignRight, f"{int(self._progress * 100 + 0.5)}%")


class QuitOnClose(QObject):
    """Quit the app when the dashboard window closes (splash/login closing must not)."""
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Close:
            QTimer.singleShot(0, QApplication.quit)
        return False


class Launcher:
    def __init__(self, app):
        self.app = app
        self.window = None
        self._quit_filter = QuitOnClose()
        self.splash = AnimatedSplash()
        self.splash.show()
        self.splash.fade(0.0, 1.0, 450)

        self.worker = StartupWorker()
        self.worker.step.connect(self.splash.set_step)
        self.worker.progress.connect(self.splash.set_progress)
        self.worker.done.connect(self._on_ready)
        self.worker.failed.connect(self._on_failed)
        QTimer.singleShot(300, self.worker.start)

    def _on_failed(self, msg):
        self.splash.set_error(msg)
        QTimer.singleShot(600, lambda: self._show_error(msg))

    def _show_error(self, msg):
        QMessageBox.critical(self.splash, "AI Digital Bodyguard", msg)
        self.app.quit()

    def _on_ready(self, token):
        if not token:
            self.splash.hide()
            dialog = LoginDialog()
            if dialog.exec() != QDialog.DialogCode.Accepted:
                self.app.quit()
                return
            api.set_token(dialog.token)
            self._open_dashboard()
        else:
            self.splash.fade(1.0, 0.0, 400, self._open_dashboard)

    def _open_dashboard(self):
        self.window = MainWindow()
        self.window.setWindowOpacity(0.0)
        self.window.resize(1200, 780)
        screen = self.app.primaryScreen().availableGeometry()
        self.window.move(screen.center() - self.window.rect().center())
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
        self.splash.close()
        self.window.installEventFilter(self._quit_filter)
        anim = QPropertyAnimation(self.window, b"windowOpacity", self.window)
        anim.setDuration(600)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self._win_anim = anim


def stop_backend():
    proc = StartupWorker.backend_proc
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AI Digital Bodyguard")
    app.setStyleSheet(DARK_STYLE)
    app.setWindowIcon(create_icon())
    app.setQuitOnLastWindowClosed(False)
    app.aboutToQuit.connect(stop_backend)
    launcher = Launcher(app)  # noqa: F841  (keep reference alive)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
