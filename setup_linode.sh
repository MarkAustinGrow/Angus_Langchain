#!/bin/bash

# Agent Angus LangChain + Coral Protocol - Linode Setup Script
# This script automates the initial setup on a fresh Linode Ubuntu server

set -e  # Exit on any error

echo "🚀 Starting Agent Angus LangChain setup on Linode..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as a regular user with sudo privileges."
   exit 1
fi

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
print_status "Installing Python 3.10+ and dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y ffmpeg libsndfile1  # For audio processing

# Install additional useful tools
print_status "Installing additional tools..."
sudo apt install -y htop nano vim ufw fail2ban

# Configure firewall
print_status "Configuring UFW firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 5555/tcp  # Coral server
sudo ufw allow 8000:8003/tcp  # Agent endpoints

print_success "Firewall configured"

# Install fail2ban for SSH protection
print_status "Configuring fail2ban..."
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Clone repository
print_status "Cloning Agent Angus LangChain repository..."
if [ -d "Angus_Langchain" ]; then
    print_warning "Directory Angus_Langchain already exists. Updating..."
    cd Angus_Langchain
    git pull origin master
else
    git clone https://github.com/MarkAustinGrow/Angus_Langchain.git
    cd Angus_Langchain
fi

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

print_success "Dependencies installed"

# Copy environment template
print_status "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Environment file created from template. Please edit .env with your credentials:"
    print_warning "nano .env"
else
    print_warning ".env file already exists. Please verify your configuration."
fi

# Make main.py executable
chmod +x main.py

# Test installation
print_status "Testing installation..."
source venv/bin/activate
python main.py --validate-config

if [ $? -eq 0 ]; then
    print_success "Installation test passed!"
else
    print_error "Installation test failed. Please check your configuration."
    exit 1
fi

# Create systemd service (optional)
read -p "Do you want to create a systemd service for auto-start? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Creating systemd service..."
    
    # Get current user and path
    CURRENT_USER=$(whoami)
    CURRENT_PATH=$(pwd)
    
    sudo tee /etc/systemd/system/angus-langchain.service > /dev/null <<EOF
[Unit]
Description=Agent Angus LangChain System
After=network.target
Wants=network.target

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_USER
WorkingDirectory=$CURRENT_PATH
Environment=PATH=$CURRENT_PATH/venv/bin
ExecStart=$CURRENT_PATH/venv/bin/python main.py --start
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable service
    sudo systemctl daemon-reload
    sudo systemctl enable angus-langchain
    
    print_success "Systemd service created and enabled"
    print_status "You can start the service with: sudo systemctl start angus-langchain"
    print_status "View logs with: sudo journalctl -u angus-langchain -f"
fi

# Setup log rotation
print_status "Setting up log rotation..."
sudo tee /etc/logrotate.d/angus-langchain > /dev/null <<EOF
$CURRENT_PATH/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 $CURRENT_USER $CURRENT_USER
    postrotate
        systemctl reload angus-langchain 2>/dev/null || true
    endscript
}
EOF

print_success "Log rotation configured"

# Display next steps
echo
echo "🎉 Setup completed successfully!"
echo
echo "📋 Next Steps:"
echo "1. Edit your environment configuration:"
echo "   nano .env"
echo
echo "2. Add your API credentials:"
echo "   - SUPABASE_URL and SUPABASE_KEY"
echo "   - OPENAI_API_KEY"
echo "   - YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_CHANNEL_ID"
echo
echo "3. Validate your configuration:"
echo "   source venv/bin/activate"
echo "   python main.py --validate-config"
echo
echo "4. Test the system:"
echo "   python main.py --start"
echo
echo "5. If you created the systemd service:"
echo "   sudo systemctl start angus-langchain"
echo "   sudo systemctl status angus-langchain"
echo
echo "📚 Documentation:"
echo "   - README.md - Complete usage guide"
echo "   - DEPLOYMENT.md - Detailed deployment instructions"
echo "   - STOP_CONTAINERS.md - Docker cleanup guide"
echo
echo "🔍 Monitoring:"
echo "   - System health: curl http://localhost:5555/health"
echo "   - Service logs: sudo journalctl -u angus-langchain -f"
echo "   - Application logs: tail -f angus_langchain.log"
echo
echo "🌐 Repository: https://github.com/MarkAustinGrow/Angus_Langchain"
echo
print_success "Agent Angus LangChain is ready for deployment!"
