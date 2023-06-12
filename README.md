# Discord File Splitter, Downloader, and Rebuilder Bot

This is a Discord bot that allows you to split files into parts, send them as messages in a text channel, download attachments from a specified channel, and rebuild a file from split parts using a record file.

## Why?
* Because I like finding loopholes in free yet limited services such as discords CDN limiting users and bots a maximum of 25MB per file, this is designed to get around it by automating the splitting, uploading, downloading, and rebuilding of large files.

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies by running the following command:

```
pip install -r requirements.txt
```

3. Create a new Discord bot and obtain the bot token. Refer to the Discord API documentation for instructions on how to create a bot and obtain the token.
4. Replace the empty string in the `bot.run('')` line of the code with your bot token.

## Usage

1. Invite the bot to your Discord server using the OAuth2 URL generated for your bot. Make sure to select the necessary permissions (e.g., read messages, send messages, manage channels, etc.) depending on the bot's functionality.
2. Launch the bot by running the Python script:

```
python main.py
```

3. The bot will be online and ready to use.

## Commands

### Split Command

Splits a file into parts and sends them as messages in a text channel.

**Syntax:** `!split <file_name>`

**Description:** This command takes a `file_name` as an argument and splits the file into parts. Each part is sent as a separate message in a text channel. The file is split into parts of 25 MB each.

### Download Command

Downloads all attachments from a specified channel to the 'downloads' directory.

**Syntax:** `!download <channel_name>`

**Description:** This command downloads all attachments from the specified `channel_name` to the 'downloads' directory. The downloaded files will be saved with their original filenames.

### Rebuild Command

Rebuilds a file from split parts using a record file.

**Syntax:** `!rebuild`

**Description:** This command prompts the user to provide the path and name of the record file. It then rebuilds the file by combining the split parts mentioned in the record file. The rebuilt file will be saved with a user-defined filename.

### List Command

Lists all available commands and their descriptions.

**Syntax:** `!list`

**Description:** This command lists all the available commands in the bot along with their syntax and a brief description of how they work.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.

## Credits
* Hall0wed - HL0#8086 on Discord

## License

This project is licensed under the [MIT License](LICENSE).
