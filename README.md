# Discord Cloud Drive Bot, aka Siamese

This is a Discord bot that allows you to split files into parts, send them as messages in a text channel, download attachments from a specified channel, and rebuild a file from split parts using a JSON database.
### Disclaimer

**This project will no long be receiving updates to https://github.com/CosmodiumCS/MK22-Siamese/ Instead go to https://github.com/d-obfuscation/Siamese Thank you.**

## Why?
Because I like finding loopholes in free yet limited services such as Discord's CDN, which limits users and bots to a maximum of 25MB per file. This bot is designed to get around this limitation by automating the splitting, uploading, downloading, and rebuilding of large files.

Note: For optimal use, please make sure you are in the MK22-Siamese directory when running main.py otherwise it can generate files/folders outside that directory in the directory you're running it from.

## Installation

1. Clone the repository
```
git clone https://github.com/CosmodiumCS/MK22-Siamese
```
2. Change directories into the repository
```
cd MK22-Siamese
```
3. Install the required dependencies by running the following command:
```
pip install -r requirements.txt
```

4. Create a new Discord bot and obtain the bot token. Refer to the Discord API documentation for instructions on how to create a bot and obtain the token.
5. Create a file called `.env` in the same directory as `main.py` and on the first line write `TOKEN=` and then paste your bot token right after the `=` without any spaces.

## Usage

1. Invite the bot to your Discord server using the OAuth2 URL generated for your bot. Make sure to select the necessary permissions (Read messages, Send messages, Manage channels, Manage Categories, Send Files).
2. Launch the bot by running the Python script:
```
python3 main.py
```

3. The bot will be online and ready to use.

## Commands

### Split Command

**Syntax:** `!split <file_name>`

**Description:** This command takes a `file_name` as an argument and splits the file into parts. Each part is sent as a separate message in a text channel. The file is split into parts of 25 MB each and a JSON entry is generated and put into `database.json` as well as a copy is pasted into the channel for you to send to others if they need to rebuild from your entry..


### Rebuild Command


**Syntax:** `!rebuild`

**Description:** This command prompts the user to make a selection from the list of entries it has in its `database.json` file and when selected, automatically pulls the files from that discord server and channel, and rebuilds it.

### List Command

**Syntax:** `!list`

**Description:** This command lists all the available commands in the bot along with their syntax and a brief description of how they work.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.

## Credits

This script was created by [Obfuscation](https://github.com/d-obfuscation) (Discord: .obf.).

## License

This project is licensed under the [MIT License](LICENSE).
