Note: The obscure name for the repo is for finding out the repo from my repo list with the client's username or using a Fiverr order ID. I wasn't that aware of using GitHub properly. As a result, you may see different names in the commit history. As I was working for different clients at the time, some of the commits seemed to have names for those accounts but the fact is those commits were made from my account and git config (user.name and user.email) were differently set as I forgot to change them before committing. As the repo was private up until now, I didn't care about the commit history. Now that I've made the project public, I thought I needed to clear those things.

# Product Scraper & Telegram Affiliate Link Remover Bot

This Telegram bot automatically removes affiliate links from messages sent in a group chat and replaces them with clean links. The bot also scrapes product information from supported websites and presents it in a user-friendly format.

## Features

* Removes affiliate links from messages sent in group chats
* Supports popular websites like Amazon, PcComponentes, Neobyte, Casemod, Coolmod, and Aussar
* Scrapes product information including name, price, image, category, and availability
* Sends product information in a user-friendly format with HTML formatting

## How it Works

The bot listens for messages in a Telegram group chat. When a message containing a supported affiliate link is detected, the bot:

1. Extracts the clean link from the affiliate link
2. Scrapes product information from the linked website
3. Deletes the original message with the affiliate link
4. Sends a new message with the clean link and scraped product information

## Requirements

* Python 3
* Required Python packages listed in `requirements.txt`
* Telegram bot token
* Chrome browser
* ChromeDriver (installed via `webdriver_manager`)

## Installation

1. Clone the repository: `git clone https://github.com/your-username/telegram-affiliate-link-remover-bot.git`
2. Install the required Python packages: `pip install -r requirements.txt`
3. Configure the bot variables in `bot_vars.py`:
    * `BOT_TOKEN`: Your Telegram bot token
    * `CHAT_IDS`: List of authorized chat IDs
    * `DEBUG_CHAT_ID`: Chat ID for debugging messages
    * `GENERAL_CHANNEL_IDS`: List of Telegram channels to share product information
    * `SHAREABLE_WEBSITES`: List of supported websites for affiliate link removal
4. Set up the database:
    * Create a SQLite database file named `db.sqlite3` in the `tg_bot_data` directory
    * The database schema is defined in `database.py`
5. Install the Chrome extension (optional):
    * Load the `chrome_extension` directory as an unpacked extension in Chrome
    * Configure the extension settings to specify the port for the Flask server
6. Start the Flask server: `python3 flask_server.py`
7. Start the scraper bot: `python3 scraper_bot.py`
8. Start the Telegram bot: `python3 tg_bot.py`

## Usage

1. Add the bot to your Telegram group chat
2. Send messages containing affiliate links from supported websites
3. The bot will automatically remove the affiliate links, scrape product information, and send a new message with clean links and product details

## Commands

* `/help`: Displays the list of available commands
* `/add`: Adds a search page link to the database
* `/delete`: Deletes a search page link from the database
* `/show`: Shows the list of search page links in the database

## Chrome Extension

The Chrome extension enhances the bot's functionality:

* Handling potential Cloudflare CAPTCHA challenges
* Providing a way to configure the Flask server port

### How it works

* When an item needs to be scraped, the URL is opened automatically using `os.system` function via Chrome browser and a Flask server starts and waits for a request to be received.
* Upon loading the URL, the Chrome extension grabs all the HTML and sends it back to the Flask server at localhost, and then it is further processed. In this way Cloudflare thinks that the request is coming from a legitimate browser and no webdrver is being used.


## Database

The bot uses a SQLite database to store:

* Search page links and their associated details (price limit, channel ID, keywords)
* Product information (name, price, image, category, availability, last sent price and time)

# Note
I also have projects where there was Cloudflare protection and other security measures that I had to prevent. If needed, I can also show them if needed.
