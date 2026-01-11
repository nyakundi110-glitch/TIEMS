# GrowattAlert - Cloud Deployment Guide

**Email Alert System for Growatt Solar Monitoring**

Send automated email alerts to your clients when solar system metrics exceed thresholds.

---

## 🚀 Quick Start - Choose Your Platform

| Platform | Difficulty | Cost | Setup Time | Best For |
|----------|-----------|------|------------|----------|
| **[PythonAnywhere](#pythonanywhere)** | ⭐ Easy | Free-$5/mo | 15 min | Beginners |
| **[Cloud VPS](#cloud-vps)** | ⭐⭐ Medium | Free-$10/mo | 30 min | Full control |
| **[Docker](#docker)** | ⭐⭐⭐ Advanced | Varies | 20 min | DevOps |

---

## What This System Does

✅ **Monitors** your Growatt solar system every 15 minutes  
✅ **Alerts** via email when power/voltage exceeds thresholds  
✅ **Reports** daily performance summaries with graphs  
✅ **Visualizes** power and voltage trends  

### Alert Conditions

- **High Power Alert**: Power >709W for 1+ hour (outside 11am-2pm)
- **Low Voltage Alert**: Battery <51V (hourly notifications)
- **Daily Report**: Comprehensive performance summary at 6 PM

---

## 📋 Prerequisites

Before deploying, you need:

1. **Growatt API Credentials**
   - Username (email)
   - Password
   - API Token
   - Plant ID
   - Device Serial Number

2. **Email Credentials**
   - Gmail account (recommended)
   - App Password ([generate here](https://myaccount.google.com/apppasswords))
   - Client email addresses for alerts

3. **Your Code**
   - Download/clone this repository

---

## 🌟 Option 1: PythonAnywhere

**Recommended for beginners** - No server management needed!

### Features
- ✅ Free tier available
- ✅ Built-in task scheduler
- ✅ No command line required
- ✅ Automatic restarts

### Limitations
- ⚠️ Free tier: Limited scheduled tasks (~10)
- ⚠️ Upgrade needed for full 15-min monitoring ($5/month)

**[→ Full PythonAnywhere Guide](file:///C:/Users/USER/.gemini/antigravity/brain/b1f7c8db-d3b4-4072-9198-2c570f195cac/DEPLOYMENT_PYTHONANYWHERE.md)**

### Quick Steps
1. Create free account at pythonanywhere.com
2. Upload your code via Files tab
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` with your credentials
5. Schedule task to run `run_monitor.py` every 15 minutes

---

## ☁️ Option 2: Cloud VPS

**Recommended for production** - Full control and flexibility!

### Platforms

#### AWS EC2
- 💰 12 months free (t2.micro)
- 🌍 Global presence
- 📈 Highly scalable

#### Google Cloud Platform
- 💰 Always-free f1-micro
- 🔒 Excellent security
- 🤖 Great ML integrations

#### DigitalOcean
- 💰 $4-6/month
- 🎯 Simple pricing
- 📚 Great documentation

**[→ Full Cloud VPS Guide](file:///C:/Users/USER/.gemini/antigravity/brain/b1f7c8db-d3b4-4072-9198-2c570f195cac/DEPLOYMENT_CLOUD_VPS.md)**

### Quick Steps
1. Create VPS instance (Ubuntu 22.04)
2. SSH into server
3. Run automated setup: `./setup_vps.sh`
4. Configure `.env` file
5. Start systemd service

---

## 🐳 Option 3: Docker

**Recommended for DevOps** - Deploy anywhere!

### Features
- ✅ Portable across platforms
- ✅ Consistent environment
- ✅ Easy updates
- ✅ Scalable

### Requirements
- Docker installed
- Docker Compose

**[→ Full Docker Guide](file:///C:/Users/USER/.gemini/antigravity/brain/b1f7c8db-d3b4-4072-9198-2c570f195cac/DEPLOYMENT_DOCKER.md)**

### Quick Steps
1. Install Docker Desktop
2. Create `.env` from template
3. Run: `docker-compose up -d`
4. Monitor: `docker-compose logs -f`

---

## 🔧 Configuration

All platforms use the same configuration via `.env` file:

```env
# Growatt API
GROWATT_USERNAME=your_email@example.com
GROWATT_PASSWORD=your_password
GROWATT_API_TOKEN=your_token
GROWATT_PLANT_ID=your_plant_id
GROWATT_DEVICE_SN=your_device_sn

# Email Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAILS=client1@example.com,client2@example.com

# Monitoring Thresholds
POWER_THRESHOLD=709
VOLTAGE_THRESHOLD=51
ENABLE_INSTANT_ALERTS=true
ENABLE_DAILY_REPORTS=true
DAILY_REPORT_TIME=18:00
```

### Getting Gmail App Password

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Sign in to your Google account
3. Select app: "Mail"
4. Select device: "Other" → Name it "GrowattAlert"
5. Click "Generate"
6. Copy the 16-character password
7. Use in `.env` as `SENDER_PASSWORD`

---

## 📊 What Gets Sent

### Email Alerts Include:

1. **Alert Type** (Power/Voltage)
2. **Current Metrics**
   - Power (W)
   - Voltage (V)
   - Timestamp
3. **Performance Graphs**
   - 24-hour power trend
   - Voltage trend
   - System dashboard

### Daily Reports Include:

1. **Summary Statistics**
   - Total energy today (kWh)
   - Peak power
   - Average power
   - Min/max voltage
   - Alert count
2. **Trend Graphs**
3. **System Status**

---

## 🎯 Customization

### Adjust Thresholds

Edit `.env`:
```env
POWER_THRESHOLD=800        # Change from 709W
VOLTAGE_THRESHOLD=50       # Change from 51V
CHECK_INTERVAL_MINUTES=30  # Change from 15 min
```

### Add More Recipients

```env
RECIPIENT_EMAILS=client1@example.com,client2@example.com,client3@example.com
```

### Change Report Time

```env
DAILY_REPORT_TIME=20:00  # 8 PM instead of 6 PM
```

---

## 🔍 Testing Your Setup

After deployment, test the system:

### 1. Test Configuration

```bash
python config_loader.py
```

Expected output:
```
✓ Configuration loaded successfully!
Growatt Account: your_email@example.com
Email Sender: your_email@gmail.com
Recipients: client@example.com
Power Threshold: 709W
Voltage Threshold: 51V
```

### 2. Test Email Connection

```bash
python email_sender.py
```

Should show: `✓ SMTP connection successful`

### 3. Manual Monitoring Run

```bash
python main.py
```

Watch logs for:
- ✅ Configuration loaded
- ✅ Connected to Growatt API
- ✅ System data retrieved
- ✅ Email sent (if alert triggered)

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Email Not Sending

**Symptom**: No emails received  
**Solutions**:
- Verify Gmail App Password (not regular password)
- Check `SENDER_EMAIL` and `SENDER_PASSWORD` in `.env`
- Test SMTP: `telnet smtp.gmail.com 587`
- Check spam folder

#### 2. Growatt API Errors

**Symptom**: "Failed to retrieve system data"  
**Solutions**:
- Verify API credentials in `.env`
- Check Plant ID and Device SN are correct
- Test API token validity

#### 3. Import Errors

**Symptom**: "ModuleNotFoundError"  
**Solutions**:
- Install requirements: `pip install -r requirements.txt`
- Use virtual environment
- Check Python version (3.8+)

---

## 📁 Project Structure

```
GrowattAlert/
├── main.py                    # Main application
├── growatt_monitor.py         # Growatt API integration
├── email_sender.py            # Email functionality
├── performance_visualizer.py  # Graph generation
├── config_loader.py          # Configuration loader
├── requirements.txt          # Python dependencies
├── .env.example             # Configuration template
├── Dockerfile               # Docker container config
├── docker-compose.yml       # Docker compose config
├── setup_vps.sh            # VPS setup script
└── growatt-monitor.service # Systemd service file
```

---

## 🔐 Security Best Practices

1. **Never commit `.env`** to version control
2. **Use App Passwords** for Gmail (not account password)
3. **Keep credentials secure** - don't share `.env`
4. **Update regularly** - keep dependencies current
5. **Monitor logs** - check for unauthorized access

---

## 📈 Monitoring Your Deployment

### Check Service Status

**PythonAnywhere**: Tasks tab → View scheduled tasks  
**VPS**: `sudo systemctl status growatt-monitor`  
**Docker**: `docker ps` and `docker logs growatt-monitor`

### View Logs

All platforms create `solar_monitor.log`:
```bash
tail -f solar_monitor.log
```

### Performance Metrics

Monitor:
- Email delivery success rate
- API connection reliability
- Alert frequency
- System uptime

---

## 🔄 Updating

### PythonAnywhere
1. Upload new files via Files tab
2. Restart scheduled tasks

### VPS
```bash
git pull origin main
sudo systemctl restart growatt-monitor
```

### Docker
```bash
docker-compose build
docker-compose up -d
```

---

## 💡 Tips for Success

1. **Start with PythonAnywhere** if you're new to hosting
2. **Test thoroughly** before relying on alerts
3. **Monitor the first week** to tune thresholds
4. **Keep backups** of your `.env` and logs
5. **Document changes** you make to configuration

---

## 📞 Support

Having issues? Check:

1. **Logs**: Most errors are visible in `solar_monitor.log`
2. **Configuration**: Verify all credentials in `.env`
3. **Platform docs**: See specific deployment guides
4. **Dependencies**: Ensure all packages installed

---

## ✅ Deployment Checklist

- [ ] Growatt API credentials obtained
- [ ] Gmail App Password generated
- [ ] Client email addresses collected
- [ ] Hosting platform selected
- [ ] `.env` file configured
- [ ] Dependencies installed
- [ ] Configuration tested (`python config_loader.py`)
- [ ] Email connection tested (`python email_sender.py`)
- [ ] System running and monitoring
- [ ] First alert received successfully
- [ ] Daily report received

---

## 🎉 You're All Set!

Your GrowattAlert system is now running in the cloud, automatically monitoring your solar system and sending alerts to your clients.

**What happens next**:
- System checks every 15 minutes
- Alerts sent when thresholds exceeded
- Daily report sent at configured time
- Logs track all activity

Enjoy automated solar monitoring! ☀️⚡📧
