# 10Books - Book Search

## Overview

This is a Discord bot written in Python using the Discord.py library and designed to search for books on Libgen (Library Genesis). The bot allows users to search for books based on title, language, and file extension, and then select a specific book from the search results to retrieve download links.

## Features

- **Book Search:** Users can search for books by providing a title, language, and file extension.
- **Interactive Selection:** The bot presents the search results in an interactive dropdown menu, allowing users to select a specific book.
- **Download Links:** After selecting a book, the bot fetches and displays download links for various file formats.

## Setup

1. **Token Configuration:**
   - Create a `settings.json` file.
   - Add your Discord bot token to the `token` field in the JSON file.

    ```json
    {
      "token": "YOUR_DISCORD_BOT_TOKEN"
    }
    ```
   
   alternatively you can use commandline arguments to run the app with your token, useful for server deployments.
   ```cmd
   python main.py -t TOKEN
   ```

2. **Libgen API:**
   - The bot uses the Libgen API for book searches. No additional configuration is required for the Libgen API.

3. **Dependencies:**
   - Install the required Python packages by running:

    ```bash
    pip install discord.py libgen-api
    ```

4. **Run the Bot:**
   - Execute the Python script to run the bot:

    ```bash
    python main.py
    ```

## Commands

- **!search:**
  - Description: Search for a book on Libgen.
  - Usage: `!search [title] --language [language] --extension [extension]`
  - Example: `!search Harry Potter --language English --extension pdf`

## Usage

1. **Search for a Book:**
   - In discord use the `/search` command to search for books based on title, language, and extension.
   - Discord formats the command automatically when inputted using the command tree

    ```
    /search Harry Potter English pdf 
    ```

2. **Select a Book or Audiobook:**
   - The bot will present the search results as an interactive dropdown menu.
   - Users can select a specific book from the menu.

3. **Retrieve Download Links:**
   - After selecting a book, the bot fetches and displays download links from various mirror links.

## Error Handling

- If an error occurs during the selection or download process, an error message will be displayed in the Discord channel, and details will be logged in the console.

## Credits

- This bot utilises the Libgen API for book searches. The Libgen API can be found [here](https://pypi.org/project/libgen-api/).

## Disclaimer

This bot is created for educational and demonstration purposes only. The use of this bot to violate any terms of service or copyright laws is strictly prohibited. The developers are not responsible for any misuse of this bot.