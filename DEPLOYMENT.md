# Linode Server Deployment Guide

This guide covers deploying Agent Angus LangChain + Coral Protocol on a Linode server.

## 🖥️ Server Requirements

### Recommended Linode Plan
- **Minimum**: Linode 4GB (Nanode 1GB may work for testing)
- **Recommended**: Linode 8GB or higher for production
- **Storage**: 25GB+ SSD storage
- **OS**: Ubuntu 22.04 LTS (recommended)

### Resource Usage
- **CPU**: Multi-core recommended for concurrent agents
- **RAM**: 4GB+ (8GB recommended for full system)
- **Network**: Stable internet connection for API calls
- **Ports**: 5555 (Coral server), 8000-8003 (agents)

## 🚀 Quick Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3 python3-pip python3-venv git curl -y

# Install system dependencies
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y

# Install audio processing libraries (for music analysis)
sudo apt install ffmpeg libsndfile1 -y
```

### 2. Clone Repository

```bash
# Clone the repository
git clone https://github.com/MarkAustinGrow/Angus_Langchain.git
cd Angus_Langchain

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (use nano, vim, or your preferred editor)
nano .env
```

**Required Environment Variables:**
```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# YouTube API Configuration
YOUTUBE_CLIENT_ID=your_youtube_oauth_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_oauth_client_secret
YOUTUBE_CHANNEL_ID=your_youtube_channel_id

# Server Configuration
CORAL_SERVER_HOST=0.0.0.0  # Listen on all interfaces
CORAL_SERVER_PORT=5555
```

### 4. Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 5555/tcp  # Coral server
sudo ufw allow 8000:8003/tcp  # Agent endpoints

# Check firewall status
sudo ufw status
```

### 5. Test Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Validate configuration
python main.py --validate-config

# Test environment
python main.py --print-env
```

## 🔧 Production Deployment

### 1. Create System User

```bash
# Create dedicated user for Agent Angus
sudo useradd -m -s /bin/bash angus
sudo usermod -aG sudo angus

# Switch to angus user
sudo su - angus

# Clone repository in user home
git clone https://github.com/MarkAustinGrow/Angus_Langchain.git
cd Angus_Langchain
```

### 2. Setup Systemd Services

Create service file for the main system:

```bash
sudo nano /etc/systemd/system/angus-langchain.service
```

```ini
[Unit]
Description=Agent Angus LangChain System
After=network.target
Wants=network.target

[Service]
Type=simple
User=angus
Group=angus
WorkingDirectory=/home/angus/Angus_Langchain
Environment=PATH=/home/angus/Angus_Langchain/venv/bin
ExecStart=/home/angus/Angus_Langchain/venv/bin/python main.py --start
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable angus-langchain

# Start the service
sudo systemctl start angus-langchain

# Check status
sudo systemctl status angus-langchain

# View logs
sudo journalctl -u angus-langchain -f
```

### 4. Setup Log Rotation

```bash
sudo nano /etc/logrotate.d/angus-langchain
```

```
/home/angus/Angus_Langchain/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 angus angus
    postrotate
        systemctl reload angus-langchain
    endscript
}
```

## 🔍 Monitoring & Maintenance

### 1. Health Checks

```bash
# Check system health
curl http://localhost:5555/health

# Check individual agents
curl http://localhost:8000/health  # Coordinator
curl http://localhost:8001/health  # YouTube
curl http://localhost:8002/health  # Database
curl http://localhost:8003/health  # AI

# Check service status
sudo systemctl status angus-langchain
```

### 2. Log Monitoring

```bash
# View real-time logs
sudo journalctl -u angus-langchain -f

# View recent logs
sudo journalctl -u angus-langchain --since "1 hour ago"

# View application logs
tail -f /home/angus/Angus_Langchain/angus_langchain.log
```

### 3. Performance Monitoring

```bash
# Check resource usage
htop

# Check disk usage
df -h

# Check memory usage
free -h

# Check network connections
netstat -tulpn | grep -E "(5555|800[0-3])"
```

## 🔄 Updates & Maintenance

### 1. Update Code

```bash
# Switch to angus user
sudo su - angus
cd Angus_Langchain

# Pull latest changes
git pull origin main

# Update dependencies if needed
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl restart angus-langchain
```

### 2. Backup Configuration

```bash
# Backup environment file
cp .env .env.backup.$(date +%Y%m%d)

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz *.log
```

### 3. Database Maintenance

```bash
# Check Supabase connection
python -c "from tools.supabase_tools import get_supabase_client; print('Connection OK' if get_supabase_client() else 'Connection Failed')"

# Clean up old logs (if using Supabase logging)
python main.py --start --agents database  # Will run cleanup tasks
```

## 🛡️ Security Considerations

### 1. Environment Security

```bash
# Secure environment file
chmod 600 .env
chown angus:angus .env

# Secure log files
chmod 640 *.log
chown angus:angus *.log
```

### 2. Network Security

```bash
# Restrict access to specific IPs (optional)
sudo ufw allow from YOUR_IP_ADDRESS to any port 5555
sudo ufw allow from YOUR_IP_ADDRESS to any port 8000:8003

# Enable fail2ban for SSH protection
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. SSL/TLS (Optional)

For production deployments, consider setting up SSL:

```bash
# Install certbot
sudo apt install certbot -y

# Get SSL certificate (if using domain)
sudo certbot certonly --standalone -d your-domain.com

# Update configuration to use SSL
# Set CORAL_SERVER_ENABLE_SSL=true in .env
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   sudo netstat -tulpn | grep 5555
   
   # Kill process if needed
   sudo kill -9 <PID>
   ```

2. **Permission Denied**
   ```bash
   # Fix ownership
   sudo chown -R angus:angus /home/angus/Angus_Langchain
   
   # Fix permissions
   chmod +x main.py
   ```

3. **Module Import Errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

4. **API Connection Issues**
   ```bash
   # Test internet connectivity
   curl -I https://api.openai.com
   curl -I https://www.googleapis.com
   
   # Check DNS resolution
   nslookup api.openai.com
   ```

### Log Analysis

```bash
# Check for errors in logs
grep -i error /home/angus/Angus_Langchain/angus_langchain.log

# Check for warnings
grep -i warning /home/angus/Angus_Langchain/angus_langchain.log

# Monitor real-time errors
tail -f /home/angus/Angus_Langchain/angus_langchain.log | grep -i error
```

## 📊 Performance Optimization

### 1. Resource Optimization

```bash
# Adjust agent limits in .env
MAX_SONGS_PER_BATCH=3  # Reduce for lower memory usage
MAX_REPLIES_PER_BATCH=5  # Reduce for lower API usage
```

### 2. Caching

```bash
# Enable result caching
CACHE_RESULTS=true
CACHE_DURATION=3600  # 1 hour
```

### 3. Rate Limiting

```bash
# Adjust rate limits for your API quotas
OPENAI_RATE_LIMIT_RPM=1000  # Reduce if hitting limits
YOUTUBE_API_CALLS_PER_MINUTE=50  # Reduce if hitting limits
```

## 🔗 Useful Commands

```bash
# Quick status check
sudo systemctl status angus-langchain

# Restart service
sudo systemctl restart angus-langchain

# View logs
sudo journalctl -u angus-langchain -f

# Check configuration
python main.py --validate-config

# Test single agent
python main.py --agent database

# Check system resources
htop

# Check disk space
df -h

# Check network connections
netstat -tulpn | grep 5555
```

## 📞 Support

If you encounter issues:

1. Check the logs: `sudo journalctl -u angus-langchain -f`
2. Validate configuration: `python main.py --validate-config`
3. Test connectivity: `curl http://localhost:5555/health`
4. Review this deployment guide
5. Check the main README.md for additional troubleshooting

---

**Note**: This deployment guide assumes you have the original Agent Angus codebase available for the YouTube and Supabase client dependencies. Make sure to update the import paths in the tools if your original codebase is in a different location.
