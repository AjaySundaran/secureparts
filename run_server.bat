@echo off
title ALGOFED SecureParts Server
echo ============================================================
echo   ALGOFED SECUREPARTS - HIGH-SECURITY WEB PLATFORM
echo ============================================================
echo [x] Enforcing Content-Security-Policy (CSP)
echo [x] Enforcing HSTS, X-Frame-Options, X-Content-Type-Options
echo [x] Active Token-Bucket Rate Limiter per Client IP
echo [x] Deterministic SHA-256 Silicon Verification Engine
echo ------------------------------------------------------------
echo Starting server on http://localhost:8080 ...
echo Press Ctrl+C to stop the server.
echo.
python server.py
pause
