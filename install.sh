#!/bin/bash
# install.sh - Set up cat-laser on a fresh Raspberry Pi after cloning the repo.
# Run as root or with sudo:  sudo bash install.sh

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="cat-laser"
SERVICE_FILE="${REPO_DIR}/contrib/cat-laser.service"
SYSTEM_SERVICE="/etc/systemd/system/${SERVICE_NAME}.service"

# ── Privilege check ──────────────────────────────────────────────────────────
if [[ $EUID -ne 0 ]]; then
    echo "Please run as root:  sudo bash install.sh"
    exit 1
fi

echo "==> Installing cat-laser from: ${REPO_DIR}"

# ── Enable I2C (required for the servo controller) ───────────────────────────
echo "==> Enabling I2C..."
if command -v raspi-config &>/dev/null; then
    raspi-config nonint do_i2c 0
    echo "    I2C enabled via raspi-config."
else
    # Fallback: edit /boot/config.txt or /boot/firmware/config.txt directly
    BOOT_CONFIG=""
    for f in /boot/firmware/config.txt /boot/config.txt; do
        if [[ -f "$f" ]]; then
            BOOT_CONFIG="$f"
            break
        fi
    done
    if [[ -n "$BOOT_CONFIG" ]]; then
        if ! grep -q "^dtparam=i2c_arm=on" "$BOOT_CONFIG"; then
            echo "dtparam=i2c_arm=on" >> "$BOOT_CONFIG"
            echo "    Added i2c_arm=on to ${BOOT_CONFIG}. A reboot will be required."
        else
            echo "    I2C already enabled in ${BOOT_CONFIG}."
        fi
    else
        echo "    WARNING: Could not find boot config file to enable I2C. Enable it manually."
    fi
fi

# ── Install Python dependencies ───────────────────────────────────────────────
echo "==> Installing Python packages..."
pip3 install -r "${REPO_DIR}/requirements.txt"

# ── Create errors directory ───────────────────────────────────────────────────
ERRORS_DIR="${REPO_DIR}/errors"
if [[ ! -d "$ERRORS_DIR" ]]; then
    mkdir -p "$ERRORS_DIR"
    echo "==> Created errors directory: ${ERRORS_DIR}"
fi

# ── Install systemd service ───────────────────────────────────────────────────
echo "==> Installing systemd service..."

# Generate a service file with the actual repo path and running user baked in
RUNNING_USER="${SUDO_USER:-pi}"
cat > "$SYSTEM_SERVICE" <<EOF
[Unit]
Description=Cat Laser
After=network.target

[Service]
WorkingDirectory=${REPO_DIR}
ExecStart=/usr/bin/python3 ${REPO_DIR}/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "    Wrote ${SYSTEM_SERVICE}"

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}.service"
systemctl restart "${SERVICE_NAME}.service"

echo ""
echo "==> Done! Service status:"
systemctl status "${SERVICE_NAME}.service" --no-pager || true

echo ""
echo "==> Cat Laser is running on port 80."
echo "    Open http://$(hostname -I | awk '{print $1}') in your browser."
echo ""
echo "    Useful commands:"
echo "      sudo systemctl status ${SERVICE_NAME}"
echo "      sudo systemctl restart ${SERVICE_NAME}"
echo "      journalctl -u ${SERVICE_NAME} -f"
