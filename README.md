# SECURE PARTS® — Universal Hardware Forensic Audit, Telemetry & Anti-Tamper Platform

A comprehensive enterprise web platform built according to the **SECURE PARTS® Comprehensive Architecture, Technology & Strategy Specification** (Target Platform: Universal Windows 10/11 x64 & ARM64).

---

## 🚀 Quick Launch

### Option 1: Double-Click Launcher (Windows)
Double-click `run_server.bat` or run in PowerShell:
```powershell
.\run_server.ps1
```
Then visit **[http://localhost:8080](http://localhost:8080)**.

### Option 2: Python Command Line
```bash
python server.py
```

### Option 3: Direct Browser Preview
Double-click [index.html](file:///c:/Users/AjaySundaran/Downloads/web/index.html) to open the platform directly in any browser.

---

## 🔑 Authentication Suite (Google + Enterprise + Signup with OTP)

Accessed via [login.html](file:///c:/Users/AjaySundaran/Downloads/web/login.html):

1. **Google Login**:
   - 1-Click Google OAuth button.
   - Connects to `/api/auth/google`, retrieves Google identity credentials, provisions or signs in the account, and issues a 32-byte cryptographic session token.

2. **Normal Own Login**:
   - Standard enterprise credentials with constant-time verification (`hmac.compare_digest`) to prevent timing side channels.
   - Default master engineering account:
     * **Email**: `lead.engineer@defense.gov`
     * **Password**: `DefenseSilicon#2026!`
   - Also supports FIDO2 / YubiKey hardware authenticator simulation.

3. **Self-Service Sign Up with 6-Digit OTP Verification**:
   - Form fields: Full Name, Enterprise Email, Organization, and Password.
   - **Step 1 (OTP Dispatch)**: Calls `/api/auth/signup/send-otp`. Generates a single-use 6-digit cryptographic code (e.g. `849201`) with a 10-minute expiry window.
   - **Step 2 (OTP Verification)**: Displays a segmented 6-digit input screen with auto-focus, countdown timer (60s), and "Resend OTP" functionality.
   - Calls `/api/auth/signup/verify-otp`. Upon verification, activates the account, commits to `USERS_DB`, and signs the user in.

---

## 🔬 Core Forensic & Verification Capabilities

1. **Online Hardware Root Verifier (`#online-verifier`)**:
   - **20-Digit Crockford Base32 Key Input**: Validates the hardware seal bound to 12 immutable roots (Motherboard UUID, CPU microcode, NVMe serials, RAM SPD, Battery IOCTL, and physical SSD Sector 2040 stamping).
   - Sample keys for testing:
     * `9D3F-8K2A-7M5N-1P4Q-0X9Z`: Lenovo ThinkPad X1 Carbon (100% Genuine Silicon).
     * `TAMPER-ALERT-SAMPLE`: HP EliteBook (Tamper Flagged: Unauthorized SATA SSD & downgraded Wi-Fi card).
   - **Steganographic PDF Certificate Validator**: Drag-and-drop tool that extracts hidden vector QR codes rendered off-canvas at coordinates `(-500, -500)` and compares them against live C++ DLL telemetry.

2. **Universal OEM Compatibility Wall (`#oem-wall`)**:
   - Interactive profile switcher for **Lenovo ThinkPad**, **Dell Precision / Latitude / XPS**, **HP EliteBook / ZBook**, **ASUS ROG**, **Apple BootCamp**, and **Framework Modular**.
   - Showcases dynamic WMI & SMBIOS probing and universal ACPI `batclass.h` IOCTL integration.

3. **System Architecture & 4 Core Pipelines (`#architecture`)**:
   - **Pipeline A**: Ultra-Fast Telemetry Acquisition (&lt; 1 µs zero-copy Win32 Shared Memory via `Local\HardwareTelemetrySharedMemV2`).
   - **Pipeline B**: Physical SSD Sector 2040 Stamping (bypasses filesystem, opens `\\.\PhysicalDrive0` directly at byte offset 1,044,480).
   - **Pipeline C**: Steganographic PDF Generation & Verification (ReportLab off-canvas vector QR).
   - **Pipeline D**: Local AI & Neural Diagnostics (Offline ONNX Runtime vector projector and threat classifier).

4. **10 Comprehensive Modules Explorer (`#modules`)**:
   - Home Dashboard, System Overview, Hardware Details, Performance Monitor, Sensors & Temperatures, System Logs, Forensic Analysis, System Reporter, Settings & Themes (Cyber Amber vs Alpine Glow), and About & Licensing.

5. **Enterprise Fleet Portal (`#fleet-portal`)**:
   - Tailored for corporate IT managers auditing 500+ heterogeneous laptops and refurbished PC retail programs (Amazon, eBay, Best Buy trade-ins).

---

## 🛡️ Enterprise Security Hardening

- **Content Security Policy (CSP)**: `default-src 'self' ...; frame-ancestors 'none'`
- **Anti-Clickjacking**: `X-Frame-Options: DENY`
- **MIME Sniffing Prevention**: `X-Content-Type-Options: nosniff`
- **HSTS Enforcement**: `Strict-Transport-Security: max-age=63072000`
- **Sliding-Window Rate Limiting**: Token-bucket per client IP to eliminate brute-force and DoS attacks.
- **Constant-Time Verification**: `hmac.compare_digest` prevents side-channel timing analysis.

---

© 2026 SECURE PARTS® Systems Engineering. All rights reserved.
