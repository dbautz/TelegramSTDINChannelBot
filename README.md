# Telegram Stdin Channel Bot

## Overview

This script allows users to send messages from standard input (stdin) to a specified Telegram channel. It's particularly useful for sending notifications, logs, or any text data directly to a Telegram channel from various sources, such as shell scripts and other programs.

## Installation

### From PyPI

You can easily install Telegram Stdin Channel Bot directly from PyPI:

```

pip install TelegramStdinChannelBot

```

This command will download and install the latest version of Telegram Stdin Channel Bot along with its dependencies.

### From Source

If you prefer to install from the source, follow these steps:

1. Clone the repository or download the source code:

```

git clone https://github.com/your-repository/telegram-stdin-bot.git

```

Or download and extract the source code to a directory of your choice.

2. Navigate to the directory where the source code is located and install the package:

```

cd telegram-stdin-bot
pip install .

```

## Prerequisites

-   Python 3.6 or higher
-   Internet connection to download dependencies

## Configuration

Before using the script, you need to configure it with your Telegram bot's API token and the channel URL where messages will be sent.

### Adding the Bot to Your Telegram Channel

1. First, ensure that your Telegram bot is a member of the channel where you want to send messages. To add the bot to a channel:

-   Go to your Telegram channel.
-   Click on the channel name at the top to view channel details.
-   Go to `Administrators` and then `Add Administrator`.
-   Search for your bot by username and add it as an administrator. Ensure the bot has permissions to send messages.

### Running the Configuration Script

2. Run the script with the `--configure` flag, and optionally `--global` to use a global configuration:

```

python telegram_stdin_bot.py --configure [--global]

```

3. Enter your Telegram bot's API token and the channel URL (e.g., `https://web.telegram.org/a/#-1002026241024`) when prompted.
4. The script will send a verification message to your Telegram channel. Enter the verification code you receive back into the script to complete the configuration.

### Configuration File Locations

-   **Windows**: The configuration file is stored in the `AppData\Roaming` directory of the current user.
-   **Linux/Unix/MacOS**: The local configuration file is stored as a hidden file in the user's home directory (e.g., `~/.telegramstdinchannelbot.ini`).
-   **Global Configuration (Optional)**: If run with the `--global` flag, the configuration will be stored in a system-wide location (`/etc` on Unix-like systems or `C:\ProgramData` on Windows).

## Usage

To send a message to your Telegram channel, simply pipe the output of any command to the script. For example:

```

echo "Hello, Telegram!" | python telegram_stdin_bot.py

```

The script will send the provided input as a message to the configured Telegram channel.

## Contributing

Contributions to this project are welcome! Please feel free to fork the repository, make changes, and submit pull requests. If you find any issues or have suggestions, please open an issue in the repository.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the license terms.

```

```
