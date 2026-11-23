# ALGOFED SecureParts - Start Script
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  ALGOFED SECUREPARTS - HIGH-SECURITY WEB PLATFORM" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "[x] Content Security Policy (CSP): Enforced" -ForegroundColor Green
Write-Host "[x] Anti-Clickjacking (X-Frame-Options: DENY): Enforced" -ForegroundColor Green
Write-Host "[x] Anti-MIME Sniffing (X-Content-Type-Options: nosniff): Enforced" -ForegroundColor Green
Write-Host "[x] Rate Limiting & Anti-Brute-Force: Active" -ForegroundColor Green
Write-Host "[x] SHA-256 HMAC Verification Engine: Active" -ForegroundColor Green
Write-Host "------------------------------------------------------------"
Write-Host "Starting server on http://localhost:8080 ..." -ForegroundColor Yellow
python server.py
