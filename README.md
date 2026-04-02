# Amazon Product Variation Scraper

## How It Works
This Python script automates the extraction of product variations (such as size and color), prices, and availability statuses from Amazon product pages. 

Because Amazon dynamically loads pricing and stock data using client-side JavaScript, standard HTML parsing libraries cannot capture this information accurately. This tool solves that by using **Playwright** to launch a Chromium browser instance. It physically navigates to the provided Amazon URL, identifies all variation buttons, systematically clicks through every possible combination, and extracts the live data directly from the updated DOM into a structured JSON format.

## Prerequisites
* Python 3.8 or higher installed on your machine.

## Setup & Installation

**1. Navigate to your project folder:**
Open your terminal and ensure you are inside the project directory:
```bash
cd product-scraper
```
**2. Create and activate a virtual environment:**
This keeps the project dependencies isolated from your main system.

On Windows:

Bash
python -m venv venv
venv\Scripts\activate
On Mac/Linux:

Bash
python3 -m venv venv
source venv/bin/activate
3. Install the required Python packages:

Bash
pip install playwright nest-asyncio
4. Install Playwright browser binaries:
This downloads the Chromium browser engine that the script uses to navigate the web.

Bash
playwright install chromium
Running the Project
To start the scraper, ensure your virtual environment is activated (venv) and run the following command:

Bash
python scraper.py
Important Usage Notes:
The CAPTCHA Window: The script is intentionally configured to run with the browser visible (headless=False). When the script starts, a browser window will open and wait for 5 seconds. Amazon frequently flags automated traffic; if a CAPTCHA appears, use this 5-second window to quickly solve it manually before the script begins its automated clicking.

Updating the Target URL: To scrape a different product, open scraper.py, locate the amazon_url variable at the bottom of the file, and replace it with your target URL. For best results, use clean URLs stripped of tracking parameters (e.g., https://www.amazon.in/dp/B0BMPLHLZ9).
