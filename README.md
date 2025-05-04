# 📩 Discord Auto Message Scheduler (Random Time)

A simple Python script that sends a daily message to a specified Discord channel at a **random time within a configurable window**.

---

## ✨ Features

- 🕒 Sends messages at a **random time** between a defined start and end time.
- 🔁 Runs continuously in the background.
- 🔧 Configuration stored in a JSON file.
- ✅ Verifies Discord token and sends test messages.
- 📅 Automatically reschedules for the next day.

---

## 📦 Requirements

- Python 3.7+
- Required libraries:

```bash
pip install requests schedule
```

---

## ⚙️ Configuration

When you first run the script, it will create a `config.json` file.

Edit it to look something like this:

```json
{
  "token": "YOUR_DISCORD_TOKEN",
  "channel_id": "YOUR_CHANNEL_ID",
  "guild_id": "YOUR_SERVER_ID",
  "message": "Hello from your automated bot!",
  "random_time_start": "09:00",
  "random_time_end": "18:00"
}
```

| Key                  | Description                                   |
|----------------------|-----------------------------------------------|
| `token`              | Your Discord user token                       |
| `channel_id`         | ID of the channel to send the message to      |
| `guild_id`           | ID of the Discord server (optional)           |
| `message`            | Content of the message                        |
| `random_time_start`  | Start of time window (format: `HH:MM`)        |
| `random_time_end`    | End of time window (format: `HH:MM`)          |

---

## 🚀 Usage

Run the script:

```bash
python main.py
```

The script will:

- Ask for your Discord token (if not already in the config)
- Let you configure channel/message/time
- Send a test message (optional)
- Start scheduling daily messages at a **random time**

> 🛑 To stop the script, press `Ctrl + C`

---

## 🧪 Example Use Case

Send a motivational message every day between 10:00 and 11:00:

```json
{
  "token": "your-token",
  "channel_id": "123456789012345678",
  "guild_id": "123456789012345678",
  "message": "Stay focused and keep coding! 💻",
  "random_time_start": "10:00",
  "random_time_end": "11:00"
}
```

---

## ⚠️ Warning

This script uses **user authentication tokens**, which may violate Discord's Terms of Service if used improperly. It's strongly recommended to use a **bot token** and operate within Discord's API guidelines.

---

