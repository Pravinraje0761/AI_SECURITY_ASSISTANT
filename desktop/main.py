import sys
import os
import time
import threading

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QSystemTrayIcon, QMenu,
    QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QWidget, QHBoxLayout, QSplashScreen
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPainter
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from services.api_client import api
from ui.styles import DARK_STYLE

BACKEND_URL = "http://127.0.0.1:8000"
DEMO_EMAIL = "demo@bodyguard.app"
DEMO_PASSWORD = "Demo12345!"


def try_demo_login():
    try:
        result = api.login(DEMO_EMAIL, DEMO_PASSWORD)
        return result["access_token"]
    except Exception:
        pass
    try:
        api.register(DEMO_EMAIL, DEMO_PASSWORD, "Demo", "User")
        result = api.login(DEMO_EMAIL, DEMO_PASSWORD)
        return result["access_token"]
    except Exception:
        return None


DEMO_SCAN_URLS = [
    "http://paypal-login-verify.xyz/account/confirm",
    "http://192.168.55.21/secure/signin",
    "https://tinyurl.com/xyzsuspicious",
    "https://github.com",
    "https://google.com",
    "http://amaz0n-update-billing.top/pay",
    "https://wikipedia.org",
]


def seed_demo_data():
    try:
        counts = api.alert_counts()
        if counts.get("total", 0) > 0:
            return
    except Exception:
        return
    try:
        api.post("/api/v1/alerts/demo-seed")
    except Exception:
        pass
    for url in DEMO_SCAN_URLS:
        try:
            api.scan_url(url)
        except Exception:
            pass


def create_icon(color="#e94560"):
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color))
    painter.drawEllipse(4, 4, 56, 56)
    painter.setBrush(QColor("white"))
    painter.setFont(QFont("Arial", 28, QFont.Weight.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "B")
    painter.end()
    return QIcon(pixmap)


def start_backend():
    import requests
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=2)
        if r.status_code == 200:
            print("[OK] Backend already running")
            return True
    except Exception:
        pass

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(project_root, "backend")
    print(f"[*] Starting backend from {backend_dir}")

    def _run():
        import subprocess
        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    t = threading.Thread(target=_run, daemon=True)
    t.start()

    import requests
    for i in range(30):
        time.sleep(1)
        try:
            r = requests.get(f"{BACKEND_URL}/health", timeout=2)
            if r.status_code == 200:
                print(f"[OK] Backend started ({i+1}s)")
                return True
        except Exception:
            pass
    print("[FAIL] Backend did not start")
    return False


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Digital Bodyguard - Login")
        self.setFixedSize(380, 300)
        self.setStyleSheet(DARK_STYLE)
        self.token = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("AI Digital Bodyguard")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #e94560;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Sign in to continue")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(subtitle)
        layout.addSpacing(10)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff4444;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)

        btn_layout = QHBoxLayout()
        login_btn = QPushButton("Sign In")
        login_btn.clicked.connect(self._login)
        register_btn = QPushButton("Register")
        register_btn.setStyleSheet("background-color: #533483;")
        register_btn.clicked.connect(self._register)
        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(register_btn)
        layout.addLayout(btn_layout)

    def _login(self):
        email = self.email.text().strip()
        password = self.password.text().strip()
        if not email or not password:
            self.error_label.setText("Fill in all fields")
            return
        try:
            result = api.login(email, password)
            self.token = result["access_token"]
            self.accept()
        except Exception as e:
            self.error_label.setText(f"Login failed: {e}")

    def _register(self):
        email = self.email.text().strip()
        password = self.password.text().strip()
        if not email or not password:
            self.error_label.setText("Fill in all fields")
            return
        try:
            api.register(email, password)
            self.error_label.setStyleSheet("color: #44ff44;")
            self.error_label.setText("Account created! Now sign in.")
        except Exception as e:
            self.error_label.setStyleSheet("color: #ff4444;")
            self.error_label.setText(f"Registration failed: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("[*] Building main window...")
        self.setWindowTitle("AI Digital Bodyguard")
        self.setMinimumSize(1000, 700)
        self.setWindowIcon(create_icon())

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        from ui.dashboard import DashboardWidget
        from ui.scanner_widget import ScannerWidget
        from ui.alerts_widget import AlertsWidget
        from ui.monitor_widget import MonitorWidget

        print("[*] Loading Dashboard...")
        self.dashboard = DashboardWidget()
        print("[*] Loading Scanner...")
        self.scanner = ScannerWidget()
        print("[*] Loading Alerts...")
        self.alerts = AlertsWidget()
        print("[*] Loading Monitor...")
        self.monitor = MonitorWidget()

        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.scanner, "Scanner")
        self.tabs.addTab(self.alerts, "Alerts")
        self.tabs.addTab(self.monitor, "System Monitor")
        self.tabs.currentChanged.connect(self._tab_changed)

        self._tray = QSystemTrayIcon(create_icon(), self)
        tray_menu = QMenu()
        tray_menu.addAction("Show").triggered.connect(self.showNormal)
        tray_menu.addSeparator()
        tray_menu.addAction("Quit").triggered.connect(QApplication.quit)
        self._tray.setContextMenu(tray_menu)
        self._tray.activated.connect(lambda reason: self.showNormal() if reason == QSystemTrayIcon.ActivationReason.DoubleClick else None)
        self._tray.setToolTip("AI Digital Bodyguard - Active")
        self._tray.show()

        self._timer = QTimer()
        self._timer.timeout.connect(self._auto_refresh)
        self._timer.start(15000)

        print("[OK] Main window ready")

    def _tab_changed(self, index):
        try:
            if index == 2:
                self.alerts._load()
            elif index == 3:
                self.monitor.refresh()
        except Exception:
            pass

    def _auto_refresh(self):
        try:
            if self.tabs.currentIndex() == 3:
                self.monitor.refresh()
        except Exception:
            pass

    def closeEvent(self, event):
        self._tray.hide()
        event.accept()


def main():
    print("=" * 50)
    print("   AI Digital Bodyguard")
    print("=" * 50)

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    app.setWindowIcon(create_icon())

    splash_pix = QPixmap(400, 250)
    splash_pix.fill(QColor("#1a1a2e"))
    sp = QPainter(splash_pix)
    sp.setPen(QColor("#e94560"))
    sp.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
    sp.drawText(splash_pix.rect(), Qt.AlignmentFlag.AlignCenter, "AI Digital Bodyguard")
    sp.setPen(QColor("#a0a0a0"))
    sp.setFont(QFont("Segoe UI", 11))
    sp.drawText(splash_pix.rect().adjusted(0, 40, 0, 40), Qt.AlignmentFlag.AlignCenter, "Starting security systems...")
    sp.end()
    splash = QSplashScreen(splash_pix)
    splash.show()
    app.processEvents()

    splash.showMessage("Starting backend...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    app.processEvents()

    if not start_backend():
        splash.close()
        QMessageBox.critical(None, "Error", "Could not start backend server.")
        sys.exit(1)

    splash.showMessage("Signing in...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
    app.processEvents()
    token = try_demo_login()

    if token:
        api.set_token(token)
        print("[*] Demo auto-login successful, launching dashboard...")
        splash.showMessage("Preparing demo data...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
        app.processEvents()
        seed_demo_data()
    else:
        dialog = LoginDialog()
        splash.finish(dialog)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)
        print("[*] Login successful, launching dashboard...")
        api.set_token(dialog.token)

    window = MainWindow()
    window.show()
    splash.finish(window)
    print("[OK] Application running")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
