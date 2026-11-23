"""
SECURE PARTS® — Central User Telemetry & Identity Console
Desktop Application built with PyQt6
Allows administrators to view, monitor, search, and export all registered users (Google SSO & Enterprise)
Includes built-in background HTTPS Cloud Telemetry receiver, local sync receiver, and file import/export.
"""

import sys
import os
import json
import time
import socket
import sqlite3
import threading
import urllib.request
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QFileDialog, QMessageBox, QComboBox, QFrame,
    QDialog, QFormLayout, QDialogButtonBox, QStatusBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt6.QtGui import QColor, QFont

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "desktop_config.json")
CLOUD_TOPIC = "secureparts-telemetry-ajaysundaran"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

def init_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            picture TEXT,
            provider TEXT DEFAULT 'google',
            organization TEXT,
            clearance TEXT,
            role TEXT,
            device TEXT DEFAULT 'Desktop',
            created_at TEXT,
            last_login TEXT
        )
    """)
    c.execute("PRAGMA table_info(users)")
    cols = [col[1] for col in c.fetchall()]
    if 'device' not in cols:
        try:
            c.execute("ALTER TABLE users ADD COLUMN device TEXT DEFAULT 'Web'")
        except Exception:
            pass

    # Ensure master seed user exists
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("""
            INSERT INTO users (id, name, email, picture, provider, organization, clearance, role, device, created_at, last_login)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "sys_master_001",
            "Dr. Sarah Chen",
            "lead.engineer@defense.gov",
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces",
            "enterprise",
            "Department of Defense / AS9100D Oversight",
            "Top Secret / SCI",
            "Principal Hardware Integrity Architect",
            "Workstation",
            "2026-01-15T09:30:00Z",
            "2026-11-22T22:56:00Z"
        ))
    conn.commit()
    conn.close()

def save_user_record(user_dict):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now_iso = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    user_id = user_dict.get("id") or user_dict.get("google_id") or user_dict.get("sub") or f"usr_{int(time.time())}"
    email = user_dict.get("email", "").strip().lower()
    if not email:
        conn.close()
        return False
    name = user_dict.get("name") or email.split("@")[0].replace(".", " ").title()
    picture = user_dict.get("picture") or user_dict.get("avatar_url") or ""
    provider = user_dict.get("provider") or "google"
    if provider.lower() == "google":
        role = "Client"
        clearance = "Client Access"
        org = user_dict.get("organization") or "Client User"
    else:
        org = user_dict.get("organization") or "Enterprise Client"
        clearance = user_dict.get("clearance") or "Level 3 - Forensic Access"
        role = user_dict.get("role") or "Systems Analyst"
    device = user_dict.get("device") or "Desktop"
    created_at = user_dict.get("created_at") or now_iso

    c.execute("""
        INSERT INTO users (id, name, email, picture, provider, organization, clearance, role, device, created_at, last_login)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET
            name=excluded.name,
            picture=COALESCE(excluded.picture, users.picture),
            last_login=excluded.last_login,
            device=COALESCE(excluded.device, users.device),
            role=COALESCE(excluded.role, users.role)
    """, (user_id, name, email, picture, provider, org, clearance, role, device, created_at, now_iso))
    conn.commit()
    conn.close()
    return True

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY last_login DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_user_by_email(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE LOWER(email) = LOWER(?)", (email.strip(),))
    conn.commit()
    conn.close()


class SyncSignalEmitter(QObject):
    user_received = pyqtSignal(dict)

SYNC_SIGNALS = SyncSignalEmitter()


class CloudSyncThread(QThread):
    user_synced = pyqtSignal(dict)
    status_updated = pyqtSignal(str)

    def __init__(self, topic=CLOUD_TOPIC):
        super().__init__()
        self.topic = topic
        self.is_running = True
        self.processed_ids = set()

    def run(self):
        self.status_updated.emit("Fetching cloud backlog...")
        self.fetch_messages(since="all")
        self.status_updated.emit("Cloud Synced (Live)")

        while self.is_running:
            time.sleep(3)
            if not self.is_running:
                break
            self.fetch_messages(since="10m")

    def fetch_messages(self, since="10m"):
        url = f"https://ntfy.sh/{self.topic}/json?poll=1&since={since}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SecurePartsAdmin/1.0"})
            with urllib.request.urlopen(req, timeout=10) as res:
                content = res.read().decode("utf-8")
                for line in content.strip().split("\n"):
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        msg_id = obj.get("id")
                        if msg_id and msg_id in self.processed_ids:
                            continue
                        if msg_id:
                            self.processed_ids.add(msg_id)

                        if obj.get("event") == "message" and obj.get("message"):
                            raw = obj.get("message")
                            user_data = json.loads(raw)
                            if isinstance(user_data, dict) and user_data.get("email"):
                                save_user_record(user_data)
                                self.user_synced.emit(user_data)
                    except Exception:
                        pass
        except Exception:
            pass

    def stop(self):
        self.is_running = False


class BackgroundSyncServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path in ["/api/users", "/api/users/"]:
            users = get_all_users()
            data = json.dumps({"success": True, "count": len(users), "users": users}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"<h1>SECURE PARTS Sync Receiver Active</h1>")

    def do_POST(self):
        if self.path in ["/api/users/sync", "/api/users/sync/"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                user_dict = json.loads(body)
                save_user_record(user_dict)
                SYNC_SIGNALS.user_received.emit(user_dict)
                response = json.dumps({"success": True, "message": "User saved to desktop database"}).encode("utf-8")
                self.send_response(200)
            except Exception as e:
                response = json.dumps({"success": False, "error": str(e)}).encode("utf-8")
                self.send_response(400)

            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def run_http_server(port=8080):
    try:
        server = HTTPServer(("0.0.0.0", port), BackgroundSyncServer)
        server.serve_forever()
    except Exception as e:
        print(f"Sync server notice (port {port}): {e}")


class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add User Manually")
        self.resize(440, 320)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #f8fafc;
            }
            QLabel {
                color: #94a3b8;
                font-size: 12px;
            }
            QLineEdit, QComboBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px 12px;
                color: #f8fafc;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #38bdf8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        title = QLabel("Register New User Record")
        title.setStyleSheet("font-size: 15px; font-weight: bold; color: #f8fafc;")
        layout.addWidget(title)

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Alex Mercer")
        form.addRow("Full Name:", self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g. alex.mercer@defense.gov")
        form.addRow("Email Address:", self.email_input)

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["google", "enterprise"])
        form.addRow("Auth Provider:", self.provider_combo)

        self.role_input = QLineEdit()
        self.role_input.setText("Hardware Forensics Analyst")
        form.addRow("Role / Title:", self.role_input)

        self.device_combo = QComboBox()
        self.device_combo.addItems(["Desktop", "Mobile", "Tablet"])
        form.addRow("Device Type:", self.device_combo)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.submit)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def submit(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        if not name or not email or "@" not in email:
            QMessageBox.warning(self, "Invalid Input", "Please provide a valid name and email address.")
            return

        save_user_record({
            "name": name,
            "email": email,
            "provider": self.provider_combo.currentText(),
            "role": self.role_input.text().strip(),
            "device": self.device_combo.currentText()
        })
        self.accept()


class SecurePartsAdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SECURE PARTS® — Central User Telemetry & Database Console")
        self.resize(1200, 740)
        self.local_ip = get_local_ip()

        # Connect background local sync signal
        SYNC_SIGNALS.user_received.connect(self.on_user_synced_event)

        self.init_ui()
        self.load_users()

        # Start Background Cloud Telemetry Receiver Thread
        self.cloud_thread = CloudSyncThread()
        self.cloud_thread.user_synced.connect(self.on_user_synced_event)
        self.cloud_thread.status_updated.connect(self.on_cloud_status)
        self.cloud_thread.start()

        # Auto-refresh timer for local DB (every 4 seconds)
        self.auto_timer = QTimer(self)
        self.auto_timer.timeout.connect(self.load_users)
        self.auto_timer.start(4000)

    def init_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0b0f19;
            }
            QWidget {
                color: #e2e8f0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            QTableWidget {
                background-color: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 12px;
                gridline-color: #1e293b;
                selection-background-color: #1e3a8a;
                selection-color: #ffffff;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 10px 12px;
                border-bottom: 1px solid #1e293b;
            }
            QTableWidget::item:hover {
                background-color: #1e293b;
            }
            QHeaderView::section {
                background-color: #1e293b;
                color: #94a3b8;
                font-weight: bold;
                font-size: 11px;
                border: none;
                border-bottom: 2px solid #334155;
                padding: 10px 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QLineEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 9px 14px;
                color: #f8fafc;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #38bdf8;
                background-color: #0f172a;
            }
            QComboBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 8px 14px;
                color: #f8fafc;
                font-size: 12px;
            }
            QPushButton {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 8px 16px;
                color: #f8fafc;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #475569;
            }
            QStatusBar {
                background-color: #0b0f19;
                color: #64748b;
                border-top: 1px solid #1e293b;
                font-family: monospace;
                font-size: 11px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(18)

        # 1. Header Bar
        header_layout = QHBoxLayout()
        header_left = QVBoxLayout()
        header_left.setSpacing(2)

        app_title = QLabel("SECURE PARTS® — Central User Telemetry Console")
        app_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #f8fafc; letter-spacing: -0.5px;")
        header_left.addWidget(app_title)

        app_sub = QLabel(f"Cross-Device Google Identity & Forensic User Registry  •  Cloud Relay: https://ntfy.sh/{CLOUD_TOPIC}")
        app_sub.setStyleSheet("font-size: 12px; color: #38bdf8; font-family: monospace;")
        header_left.addWidget(app_sub)

        header_layout.addLayout(header_left)
        header_layout.addStretch()

        # Status badge
        status_box = QFrame()
        status_box.setStyleSheet("background-color: #064e3b; border: 1px solid #059669; border-radius: 20px; padding: 4px 14px;")
        status_box_layout = QHBoxLayout(status_box)
        status_box_layout.setContentsMargins(6, 4, 6, 4)
        dot = QLabel("●")
        dot.setStyleSheet("color: #34d399; font-size: 14px; margin-right: 2px;")
        self.status_badge_lbl = QLabel("CLOUD & LOCAL SYNC ACTIVE")
        self.status_badge_lbl.setStyleSheet("color: #a7f3d0; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;")
        status_box_layout.addWidget(dot)
        status_box_layout.addWidget(self.status_badge_lbl)
        header_layout.addWidget(status_box)

        main_layout.addLayout(header_layout)

        # 2. Metric KPI Cards Row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)

        self.card_total = self.create_kpi_card("TOTAL USERS", "0", "#38bdf8", "👥")
        self.card_google = self.create_kpi_card("GOOGLE SSO", "0", "#60a5fa", "🌐")
        self.card_mobile = self.create_kpi_card("MOBILE SIGN-INS", "0", "#a78bfa", "📱")
        self.card_desktop = self.create_kpi_card("DESKTOP USERS", "0", "#34d399", "💻")

        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_google)
        cards_layout.addWidget(self.card_mobile)
        cards_layout.addWidget(self.card_desktop)

        main_layout.addLayout(cards_layout)

        # 3. Search & Control Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search users by name, email, role, or device...")
        self.search_input.textChanged.connect(self.filter_table)
        toolbar.addWidget(self.search_input, stretch=3)

        self.provider_filter = QComboBox()
        self.provider_filter.addItems(["All Providers", "Google SSO Only", "Enterprise Only"])
        self.provider_filter.currentIndexChanged.connect(self.filter_table)
        toolbar.addWidget(self.provider_filter, stretch=1)

        self.btn_cloud_sync = QPushButton("☁️ Sync Cloud")
        self.btn_cloud_sync.clicked.connect(self.manual_cloud_sync)
        self.btn_cloud_sync.setStyleSheet("background-color: #2563eb; color: white; border: none;")
        toolbar.addWidget(self.btn_cloud_sync)

        self.btn_import = QPushButton("📂 Import File")
        self.btn_import.clicked.connect(self.import_file)
        toolbar.addWidget(self.btn_import)

        self.btn_add = QPushButton("➕ Add User")
        self.btn_add.clicked.connect(self.open_add_user_dialog)
        self.btn_add.setStyleSheet("background-color: #0284c7; color: white; border: none;")
        toolbar.addWidget(self.btn_add)

        self.btn_export_csv = QPushButton("📥 Export CSV")
        self.btn_export_csv.clicked.connect(self.export_csv)
        toolbar.addWidget(self.btn_export_csv)

        self.btn_export_json = QPushButton("📊 Export JSON")
        self.btn_export_json.clicked.connect(self.export_json)
        toolbar.addWidget(self.btn_export_json)

        main_layout.addLayout(toolbar)

        # 4. Central Data Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "User Profile", "Email Address", "Provider", "Device",
            "Role / Designation", "Security Clearance", "Registered At", "Actions"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table)

        # 5. Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready. Connected to Cloud Telemetry & listening for cross-device sign-ins.")

    def create_kpi_card(self, title, initial_value, color_hex, emoji):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 12px 16px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        top_row = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 11px; font-weight: 700; color: #94a3b8; font-family: monospace;")
        icon_lbl = QLabel(emoji)
        icon_lbl.setStyleSheet("font-size: 16px;")
        top_row.addWidget(t_lbl)
        top_row.addStretch()
        top_row.addWidget(icon_lbl)
        layout.addLayout(top_row)

        val_lbl = QLabel(initial_value)
        val_lbl.setObjectName("value_label")
        val_lbl.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {color_hex};")
        layout.addWidget(val_lbl)

        return card

    def update_kpi_card(self, card, new_value):
        lbl = card.findChild(QLabel, "value_label")
        if lbl:
            lbl.setText(str(new_value))

    def on_cloud_status(self, msg):
        self.status_badge_lbl.setText(msg.upper())

    def on_user_synced_event(self, user_dict):
        name = user_dict.get("name", "User")
        email = user_dict.get("email", "")
        device = user_dict.get("device", "Device")
        self.status_bar.showMessage(f"⚡ Sign-in captured: {name} ({email}) from {device}!", 8000)
        self.load_users()

    def manual_cloud_sync(self):
        self.status_bar.showMessage("Syncing from Cloud Relay...", 3000)
        self.cloud_thread.fetch_messages(since="all")
        self.load_users()
        self.status_bar.showMessage("Cloud synchronization complete!", 5000)

    def load_users(self):
        users = get_all_users()
        total_count = len(users)
        google_count = sum(1 for u in users if (u.get("provider") or "").lower() == "google")
        mobile_count = sum(1 for u in users if (u.get("device") or "").lower() == "mobile")
        desktop_count = total_count - mobile_count

        self.update_kpi_card(self.card_total, total_count)
        self.update_kpi_card(self.card_google, google_count)
        self.update_kpi_card(self.card_mobile, mobile_count)
        self.update_kpi_card(self.card_desktop, desktop_count)

        self.current_users = users
        self.filter_table()

    def filter_table(self):
        query = self.search_input.text().strip().lower()
        provider_filter_idx = self.provider_filter.currentIndex()

        filtered = []
        for u in getattr(self, "current_users", []):
            name = (u.get("name") or "").lower()
            email = (u.get("email") or "").lower()
            role = (u.get("role") or "").lower()
            device = (u.get("device") or "").lower()
            provider = (u.get("provider") or "").lower()

            if provider_filter_idx == 1 and provider != "google":
                continue
            if provider_filter_idx == 2 and provider == "google":
                continue

            if query and not (query in name or query in email or query in role or query in device):
                continue

            filtered.append(u)

        self.populate_table(filtered)

    def populate_table(self, users):
        self.table.setRowCount(len(users))
        for row_idx, u in enumerate(users):
            # 0. User Profile
            name = u.get("name") or "User"
            item_name = QTableWidgetItem(name)
            item_name.setFont(QFont("", 11, QFont.Weight.Bold))
            self.table.setItem(row_idx, 0, item_name)

            # 1. Email Address
            email = u.get("email") or ""
            item_email = QTableWidgetItem(email)
            item_email.setForeground(QColor("#38bdf8"))
            self.table.setItem(row_idx, 1, item_email)

            # 2. Provider Badge
            provider = (u.get("provider") or "google").upper()
            item_provider = QTableWidgetItem(f"  {provider}  ")
            item_provider.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if provider == "GOOGLE":
                item_provider.setBackground(QColor("#1e3a8a"))
                item_provider.setForeground(QColor("#93c5fd"))
            else:
                item_provider.setBackground(QColor("#064e3b"))
                item_provider.setForeground(QColor("#a7f3d0"))
            self.table.setItem(row_idx, 2, item_provider)

            # 3. Device Badge
            device = u.get("device") or "Desktop"
            item_device = QTableWidgetItem(f"📱 {device}" if device.lower() == "mobile" else f"💻 {device}")
            self.table.setItem(row_idx, 3, item_device)

            # 4. Role
            role = u.get("role") or "Analyst"
            self.table.setItem(row_idx, 4, QTableWidgetItem(role))

            # 5. Clearance
            clearance = u.get("clearance") or "Level 3"
            self.table.setItem(row_idx, 5, QTableWidgetItem(clearance))

            # 6. Registered At
            created_at = u.get("created_at") or ""
            date_display = created_at[:10] if len(created_at) >= 10 else created_at
            self.table.setItem(row_idx, 6, QTableWidgetItem(date_display))

            # 7. Action Button (Delete)
            del_btn = QPushButton("🗑️ Delete")
            del_btn.setStyleSheet("background-color: #450a0a; color: #fca5a5; border: 1px solid #7f1d1d; border-radius: 6px; padding: 4px 8px; font-size: 11px;")
            del_btn.clicked.connect(lambda checked, em=email: self.delete_user(em))
            self.table.setCellWidget(row_idx, 7, del_btn)

    def delete_user(self, email):
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to remove user:\n{email}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            delete_user_by_email(email)
            self.load_users()
            self.status_bar.showMessage(f"User {email} deleted from database.", 5000)

    def open_add_user_dialog(self):
        dialog = AddUserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_users()
            self.status_bar.showMessage("New user added successfully.", 5000)

    def import_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Users Database", "",
            "Data Files (*.json *.csv);;JSON Files (*.json);;CSV Files (*.csv)"
        )
        if not path:
            return
        imported = 0
        try:
            if path.endswith(".json"):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for u in data:
                            if isinstance(u, dict) and u.get("email"):
                                save_user_record(u)
                                imported += 1
            elif path.endswith(".csv"):
                import csv
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        u = {
                            "id": row.get("ID") or row.get("User ID"),
                            "name": row.get("Name"),
                            "email": row.get("Email"),
                            "provider": row.get("Provider"),
                            "device": row.get("Device"),
                            "organization": row.get("Organization"),
                            "clearance": row.get("Clearance"),
                            "role": row.get("Role")
                        }
                        if u.get("email"):
                            save_user_record(u)
                            imported += 1
            self.load_users()
            QMessageBox.information(self, "Import Successful", f"Successfully imported {imported} users into database.")
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import file: {e}")

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Users to CSV", "secureparts_users.csv", "CSV Files (*.csv)")
        if path:
            users = get_all_users()
            import csv
            try:
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Name", "Email", "Provider", "Device", "Organization", "Clearance", "Role", "Created At", "Last Login"])
                    for u in users:
                        writer.writerow([
                            u.get("id"), u.get("name"), u.get("email"), u.get("provider"),
                            u.get("device"), u.get("organization"), u.get("clearance"),
                            u.get("role"), u.get("created_at"), u.get("last_login")
                        ])
                QMessageBox.information(self, "Export Successful", f"Exported {len(users)} users to:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Could not write CSV: {e}")

    def export_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Users to JSON", "secureparts_users.json", "JSON Files (*.json)")
        if path:
            users = get_all_users()
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(users, f, indent=2)
                QMessageBox.information(self, "Export Successful", f"Exported {len(users)} users to:\n{path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Could not write JSON: {e}")

    def closeEvent(self, event):
        if hasattr(self, 'cloud_thread'):
            self.cloud_thread.stop()
            self.cloud_thread.wait(1000)
        event.accept()


def main():
    init_database()

    sync_thread = threading.Thread(target=run_http_server, args=(8080,), daemon=True)
    sync_thread.start()

    app = QApplication(sys.argv)
    window = SecurePartsAdminWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
