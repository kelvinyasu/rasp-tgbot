# Raspberry Pi Telegram Bot (rasp-tgbot)

A Python-based Telegram bot designed for personal server management and monitoring on Raspberry Pi devices. This bot provides remote access to system information, control commands, and automated maintenance features.

## Features

### System Commands
- **`/roll`** - Roll a dice (1-6)
- **`/time`** - Get current system time
- **`/reboot`** - Stop VPN and reboot the system (with 2-second delay)
- **`/network`** - Display network interfaces and IP addresses (internal and external)
- **`/syslog`** - Show last 20 lines of system log
- **`/chatid`** - Display your chat ID for whitelist management
- **`/upgrade`** - Pull latest code from Git repository and schedule service restart

### Security Features
- **Whitelist-based access control** - Only authorized chat IDs can interact with the bot
- **Automatic chat ID logging** - New users are automatically added to the whitelist
- **System log integration** - All commands are logged to syslog

### System Integration
- **Systemd service** - Runs as a system service with automatic restart
- **Timer-based startup** - Delayed startup after boot for network stability
- **Git-based updates** - Self-updating capability with version tracking
- **MOTD support** - Customizable message of the day

## Installation

### Prerequisites
- Raspberry Pi running Linux
- Python 3.x
- Telegram Bot Token (obtain from [@BotFather](https://t.me/botfather))
- Git
- Systemd (for service management)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rasp-tgbot
   ```

2. **Install to system directory:**
   ```bash
   sudo mkdir -p /usr/local/bin/tgbot
   sudo cp *.py /usr/local/bin/tgbot/
   sudo cp *.txt /usr/local/bin/tgbot/
   sudo cp *.sh /usr/local/bin/tgbot/
   sudo chmod +x /usr/local/bin/tgbot/restartservice.sh
   ```

3. **Configure bot token:**
   ```bash
   sudo nano /usr/local/bin/tgbot/bot.txt
   # Replace YOUR-TG-BOT-TOKEN-HERE with your actual bot token
   ```

4. **Customize MOTD (optional):**
   ```bash
   sudo nano /usr/local/bin/tgbot/botmotd.txt
   # Add your custom welcome message
   ```

5. **Install systemd service:**
   ```bash
   sudo cp startupservice/* /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable telegram_bot.service
   sudo systemctl enable telegram_bot.timer
   ```

6. **Start the service:**
   ```bash
   sudo systemctl start telegram_bot.timer
   ```

## Configuration

### File Structure
```
/usr/local/bin/tgbot/
├── telegram_bot.py      # Main bot logic
├── startbot.py          # Service entry point
├── bot.txt              # Bot token (keep secure!)
├── botmotd.txt          # Message of the day
├── chat_ids.txt         # Whitelist of authorized chat IDs
└── restartservice.sh    # Service restart script
```

### Environment Variables
- `SCRIPT_VERSION` - Bot version (currently 0.31)
- `CHAT_ID_FILE` - Path to whitelist file
- `GIT_COMMIT_HASH` - Current Git commit hash

## Usage

### First Time Setup
1. Start a conversation with your bot on Telegram
2. Send any command (e.g., `/chatid`)
3. Your chat ID will be automatically added to the whitelist
4. You can now use all bot commands

### Command Examples
```
/roll          # Returns: 4
/time          # Returns: 2024-01-15 14:30:25.123456
/network       # Returns: Network interfaces and IP addresses
/syslog        # Returns: Last 20 lines of system log
/reboot        # Returns: Stop VPN & Rebooting...
/upgrade       # Returns: Bot scheduled upgrade...
```

## Service Management

### Manual Control
```bash
# Start service
sudo systemctl start telegram_bot.service

# Stop service
sudo systemctl stop telegram_bot.service

# Restart service
sudo systemctl restart telegram_bot.service

# Check status
sudo systemctl status telegram_bot.service

# View logs
sudo journalctl -u telegram_bot.service -f
```

### Automatic Startup
The bot is configured to start automatically 2 minutes after boot via systemd timer.

## Security Considerations

- **Bot Token Security**: Keep your bot token secure and never commit it to version control
- **Whitelist Management**: Only authorized chat IDs can interact with the bot
- **System Access**: The bot runs with root privileges for system commands
- **Network Security**: Consider VPN or firewall rules for additional protection

## Troubleshooting

### Common Issues

1. **Bot not responding:**
   - Check if service is running: `sudo systemctl status telegram_bot.service`
   - Verify bot token is correct in `/usr/local/bin/tgbot/bot.txt`
   - Check logs: `sudo journalctl -u telegram_bot.service`

2. **Permission denied errors:**
   - Ensure bot files have correct permissions
   - Check if running as root user

3. **Network commands failing:**
   - Verify network connectivity
   - Check if required tools are installed (`ip`, `curl`)

### Logs
- Service logs: `sudo journalctl -u telegram_bot.service`
- System logs: `/var/log/syslog`
- Bot logs: Check syslog for entries with identifier `telegram_bot`

## Development

### Version Information
- Current version: 0.31
- Git integration for automatic updates
- Version tracking via commit hash

### Contributing
1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is for personal use. Please ensure compliance with Telegram's Terms of Service and your local laws when using this bot.

## Disclaimer

This bot provides remote access to your system. Use responsibly and ensure proper security measures are in place. The authors are not responsible for any misuse or damage caused by this software.
