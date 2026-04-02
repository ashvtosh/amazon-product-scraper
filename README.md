# Amazon Product Variation Scraper

## Overview
This project is an asynchronous Python web scraper that uses Playwright to extract structured product data from Amazon. Given a product URL, the script dynamically clicks through all available product variations (e.g., color and size combinations) and captures the specific price and availability status for each combination.

## Features
* **Dynamic Interaction:** Simulates human interaction by physically clicking variation buttons on the page rather than relying on static HTML parsing.
* **Efficient Execution:** Avoids redundant full-page reloads by extracting updated DOM elements (`price`, `stock`) immediately after client-side JavaScript updates the page.
* **JSON Output:** Formats the scraped data into a clean, structured JSON response.

## Prerequisites
* Python 3.8+

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd product-scraper
