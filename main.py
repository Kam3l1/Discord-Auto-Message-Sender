import os
import random
import time
from datetime import datetime
import json
import requests
import schedule
import threading

# config
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "token": " ",
    "channel_id": " ",  # Channel ID
    "guild_id": " ",    # Server ID
    "message": " ",           # Message
    "random_time_start": " ",         # Random start time
    "random_time_end": " "            # Random end time
}

# config initialization
def init_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"Created Config File {CONFIG_FILE}")
        print("Please put your discord account token in the config.json file")
        return False
    return True

# config loading
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# config saving
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# downloading discord token
def get_discord_token():
    config = load_config()
    token = config.get("token", "")
    
    if not token:
        token = input("Enter your discord token: ")
        config["token"] = token
        save_config(config)
    
    return token

# sending messages in discord channel
def send_message(token, channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "content": message
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Message sent successfully")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error sending message: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Exception while sending: {e}")
        return False

# Checking if the token is correct
def check_token(token):
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": token
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"Logged in as: {user_data.get('username')}#{user_data.get('discriminator')}")
            return True
        else:
            print(f"Error while veryfing token: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Exception while veryfing token: {e}")
        return False

# Time planning function
def schedule_random_time(config):
    # Time randomizer
    start_hour, start_minute = map(int, config["random_time_start"].split(':'))
    end_hour, end_minute = map(int, config["random_time_end"].split(':'))
    
    # Conversion in minutes for better randomization
    start_total_minutes = start_hour * 60 + start_minute
    end_total_minutes = end_hour * 60 + end_minute
    
    # Drawing the number of minutes
    random_minutes = random.randint(start_total_minutes, end_total_minutes)
    
    # Convert back to hours and minutes
    random_hour = random_minutes // 60
    random_minute = random_minutes % 60
    
    # Formatting to record time
    random_time = f"{random_hour:02d}:{random_minute:02d}"
    
    print(f"The message was scheduled to be sent at{random_time}")
    
    # Scheduling a task for a randomly selected time
    schedule.every().day.at(random_time).do(
        send_message, config["token"], config["channel_id"], config["message"]
    )

# Scheduling a new random time for the next day
def schedule_for_tomorrow(config):
    # Clearing previous tasks
    schedule.clear()
    
    # Scheduling a new random time for the next day
    schedule_random_time(config)
    
    print("A message was scheduled for the next day")

# Launching the planner in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# The main function of the program
def main():
    print("=== Discord Auto Message (with random time) ===")
    
    # Initialization and loading of configuration
    if not init_config():
        input("Press Enter to finish...")
        return
    
    config = load_config()
    
    # If the token is empty, ask for it to be entered
    if not config["token"]:
        config["token"] = input("Enter your Discord token: ")
        save_config(config)
    
    # Token verification
    if not check_token(config["token"]):
        print("Invalid Discord token. Please check your configuration.")
        # Removing invalid token
        config["token"] = ""
        save_config(config)
        input("Press Enter to finish...")
        return
    
    # Displaying the current configuration
    print("\nCurrent configuration:")
    print(f"Channel ID: {config['channel_id']}")
    print(f"Server ID: {config['guild_id']}")
    print(f"Message: {config['message']}")
    print(f"Time frame: {config['random_time_start']} - {config['random_time_end']}")
    
    # Option to change configuration
    if input("\nDo you want to change the configuration? (y/n): ").lower() == 'y':
        config["channel_id"] = input(f"ID Channel [{config['channel_id']}]: ") or config["channel_id"]
        config["guild_id"] = input(f"ID Server [{config['guild_id']}]: ") or config["guild_id"]
        config["message"] = input(f"message [{config['message']}]: ") or config["message"]
        config["random_time_start"] = input(f"Start of time period [{config['random_time_start']}]: ") or config["random_time_start"]
        config["random_time_end"] = input(f"End of time period [{config['random_time_end']}]: ") or config["random_time_end"]
        save_config(config)
        print("Configuration updated.")
    
    # Option to send a test message
    if input("\nSend a test message now? (y/n): ").lower() == 'y':
        if send_message(config["token"], config["channel_id"], f"Test message: {config['message']}"):
            print("Message test successful!")
        else:
            print("Message test failed.")
            input("Press Enter to finish...")
            return
    
    # Scheduling a random time for today
    schedule_random_time(config)
    
    # Scheduling a task that will schedule a new random time for the next day at midnight every day
    schedule.every().day.at("00:01").do(schedule_for_tomorrow, config)
    
    # Launching the planner in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    print("\nThe program runs in the background. The message will be sent every day at a random time.")
    print("Press Ctrl+C to exit.")
    
    try:
        # Maintaining the main thread
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting program...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to finish...")