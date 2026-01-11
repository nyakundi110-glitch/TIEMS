#!/bin/bash
# Automated setup script for GrowattAlert on Ubuntu/Debian VPS

set -e  # Exit on error

echo "========================================="
echo "GrowattAlert VPS Setup Script"
echo "========================================="
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python and dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv git

# Create application directory
APP_DIR="/home/$USER/GrowattAlert"
echo "📁 Creating application directory: $APP_DIR"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📚 Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📂 Creating logs and data directories..."
mkdir -p logs data

# Setup environment file
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your credentials:"
    echo "    nano .env"
    echo ""
    read -p "Press Enter to edit .env now, or Ctrl+C to do it later..."
    nano .env
fi

# Install systemd service
echo "🔄 Installing systemd service..."
sudo cp growatt-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable growatt-monitor.service

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Verify your .env configuration:"
echo "   nano $APP_DIR/.env"
echo ""
echo "2. Test the configuration:"
echo "   source $APP_DIR/venv/bin/activate"
echo "   python config_loader.py"
echo ""
echo "3. Start the service:"
echo "   sudo systemctl start growatt-monitor"
echo ""
echo "4. Check service status:"
echo "   sudo systemctl status growatt-monitor"
echo ""
echo "5. View logs:"
echo "   tail -f $APP_DIR/logs/service.log"
echo ""
