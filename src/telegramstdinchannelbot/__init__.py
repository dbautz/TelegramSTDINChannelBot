import argparse
import configparser
import os
import platform
import random
import re
import sys

import requests


class TelegramBotConfig:
    """
    Manages configuration for the Telegram bot.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.config = configparser.ConfigParser()

    def load_config(self):
        """
        Loads the configuration from the configuration file.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                "Configuration file not found.\n"
                "Please run 'python telegram_stdin_bot.py --configure' to set up the configuration."
            )

        self.config.read(self.filepath)

    def save_config(self, api_token, channel_id):
        """
        Saves the Telegram API token and channel ID to the configuration file.
        Validates the token and ID before saving.
        """
        if not self._is_valid_api_token(api_token):
            raise ValueError("Invalid API token format.")

        if not self._is_valid_channel_id(channel_id):
            raise ValueError("Invalid channel ID format.")

        self.config["DEFAULT"] = {
            "TELEGRAM_API_TOKEN": api_token,
            "TELEGRAM_CHANNEL_ID": channel_id,
        }

        with open(self.filepath, "w") as configfile:
            self.config.write(configfile)

    def get_api_token(self):
        """
        Returns the Telegram API token from the configuration.
        """
        return self.config["DEFAULT"]["TELEGRAM_API_TOKEN"]

    def get_channel_id(self):
        """
        Returns the Telegram channel ID from the configuration.
        """
        return self.config["DEFAULT"]["TELEGRAM_CHANNEL_ID"]

    def _is_valid_api_token(self, token):
        """
        Validates the API token format.
        """
        pattern = r"\d+:[\w-]+"
        return re.match(pattern, token) is not None

    def _is_valid_channel_id(self, channel_id):
        """
        Validates the channel ID format.
        """
        pattern = r"(-[0-9]+)"
        return re.match(pattern, channel_id) is not None


class TelegramBot:
    """
    Handles operations of a Telegram bot.
    """

    def __init__(self, config):
        self.config = config

    def send_message(self, text):
        """
        Sends a message to the specified Telegram channel.
        """
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{self.config.get_api_token()}/sendMessage",
                params={"chat_id": self.config.get_channel_id(), "text": text},
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to send message. Error: {e}")
            sys.exit(1)


def get_global_config_path():
    """
    Returns the path to the global configuration file, depending on the operating system.
    """
    if platform.system() == "Windows":
        program_data = os.environ.get("PROGRAMDATA", "C:\\ProgramData")
        config_path = os.path.join(program_data, "TelegramStdinChannelBot", "config.ini")
    else:  # Unix-like systems
        config_path = "/etc/telegramstdinchannelbot.ini"

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    return config_path


def get_local_config_path():
    """
    Returns the path to the local configuration file.
    On Windows, this will be in the user's AppData directory.
    On Unix-like systems, it will be a hidden file in the user's home directory.
    """
    if platform.system() == "Windows":
        app_data = os.environ.get(
            "APPDATA", os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
        )
        config_path = os.path.join(app_data, "TelegramStdinChannelBot", "config.ini")
    else:  # Unix-like systems (Linux, MacOS)
        home_dir = os.path.expanduser("~")
        config_path = os.path.join(home_dir, ".telegramstdinchannelbot.ini")

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    return config_path


def configure_telegram(config, telegram_bot):
    """
    Configures the Telegram bot by setting its API token and extracting the channel ID from the provided URL.
    Includes a verification step by sending a test message.
    """
    api_token = input("Enter Telegram API token: ")
    channel_url = input(
        "Enter the Telegram channel URL (e.g., https://web.telegram.org/a/#-1002026241024): "
    )

    # Extract the channel ID from the URL
    match = re.search(r"(-\d+)$", channel_url)
    if not match:
        print("Invalid channel URL format.")
        sys.exit(1)

    channel_id = match.group(1)

    verification_number = random.randint(1000, 9999)
    message = f"Your verification code is: {verification_number}"

    try:
        config.save_config(api_token, channel_id)
        telegram_bot.send_message(message)
        print("A verification message has been sent to your Telegram channel.")

        user_input = input("Please enter the verification code you received: ")
        if str(verification_number) != user_input.strip():
            raise ValueError("Verification failed. The entered number does not match.")

        print("Verification successful! Your bot is now configured.")

    except ValueError as e:
        print(f"Error during configuration: {e}")
        sys.exit(1)


def handle_stdin(telegram_bot):
    """
    Handles standard input and sends it as messages to the Telegram channel.
    """
    if sys.stdin.isatty():
        print("No stdin provided. Please pipe the text you want to send into the script.")
        sys.exit(1)

    stdin = sys.stdin.read()
    stdin_list = [stdin[i : i + 4096] for i in range(0, len(stdin), 4096)]
    for message in stdin_list:
        telegram_bot.send_message(message)


def main():
    argparser = argparse.ArgumentParser(description="Send stdin to Telegram")
    argparser.add_argument(
        "--configure", action="store_true", help="Configure the Telegram API token and channel ID"
    )
    argparser.add_argument(
        "--global", dest="use_global_config", action="store_true", help="Use global configuration"
    )
    args = argparser.parse_args()

    if args.use_global_config:
        config_path = get_global_config_path()
    else:
        config_path = get_local_config_path()

    config = TelegramBotConfig(config_path)

    if args.configure:
        telegram_bot = TelegramBot(config)  # Initialize the bot with the config
        configure_telegram(config, telegram_bot)
    else:
        try:
            config.load_config()
            telegram_bot = TelegramBot(config)
            handle_stdin(telegram_bot)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)
        except KeyError:
            print(
                "Invalid configuration found. Please ensure the configuration file is correctly formatted.\n"
                "Run 'python telegram_stdin_bot.py --configure' to reset the configuration."
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
