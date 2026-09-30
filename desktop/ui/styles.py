import sys
import os
import json

DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #1a1a2e;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QLabel { color: #e0e0e0; }
QPushButton {
    background-color: #0f3460;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover { background-color: #16213e; }
QPushButton:pressed { background-color: #533483; }
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #0f3460;
    border-radius: 4px;
    padding: 6px;
}
QLineEdit:focus, QTextEdit:focus { border: 1px solid #533483; }
QTableWidget {
    background-color: #16213e;
    color: #e0e0e0;
    gridline-color: #0f3460;
    border: none;
    border-radius: 4px;
}
QTableWidget::item { padding: 6px; }
QTableWidget::item:selected { background-color: #533483; }
QHeaderView::section {
    background-color: #0f3460;
    color: white;
    padding: 6px;
    border: none;
    font-weight: bold;
}
QTabWidget::pane { border: none; background-color: #1a1a2e; }
QTabBar::tab {
    background-color: #16213e;
    color: #a0a0a0;
    padding: 10px 20px;
    border: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #533483;
    color: white;
}
QScrollBar:vertical {
    background-color: #1a1a2e;
    width: 10px;
}
QScrollBar::handle:vertical {
    background-color: #0f3460;
    border-radius: 5px;
    min-height: 20px;
}
QMessageBox { background-color: #1a1a2e; }
QGroupBox {
    border: 1px solid #0f3460;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 15px;
    color: #e0e0e0;
    font-weight: bold;
}
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
QComboBox {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #0f3460;
    border-radius: 4px;
    padding: 5px;
}
"""
