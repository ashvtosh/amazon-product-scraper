import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_amazon_product(url):
    print(f"Starting Amazon scraper for: {url}")
    
    async with async_playwright() as p:
        # We MUST keep headless=False for Amazon. They often throw a CAPTCHA on the first load.
        # This allows you to manually click the CAPTCHA if needed!
        browser = await p.chromium.launch(headless=False) 
        
        # Adding extra viewport and user-agent settings to look more like a real human
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        try:
            print("Navigating to Amazon...")
            await page.goto(url, wait_until="domcontentloaded")
            
            # Pause to let you solve a CAPTCHA if Amazon asks for one
            print("Waiting 5 seconds to bypass potential CAPTCHAs...")
            await page.wait_for_timeout(5000) 
            
            print("Extracting product information...")
            
            # 1. Get Product Name (Amazon uses the ID #productTitle)
            product_name_element = page.locator('#productTitle')
            product_name = await product_name_element.inner_text() if await product_name_element.count() > 0 else "Unknown Amazon Product"
            
            results = {
                "product_name": product_name.strip(),
                "variations": []
            }

            # 2. Locate Variation Buttons
            # Amazon typically wraps variation lists in these specific IDs
            color_buttons = await page.locator('#variation_color_name li button').all()
            size_buttons = await page.locator('#variation_size_name li button').all()

            print(f"Found {len(color_buttons)} colors and {len(size_buttons)} sizes.")

            # If there are no variations, just grab the base price
            if not color_buttons and not size_buttons:
                print("No variations found. Grabbing base price.")
                # Base price extraction logic would go here
                
            # 3. Iterate through combinations
            for color_btn in color_buttons:
                # Amazon buttons can be tricky, force the click
                await color_btn.click(force=True)
                
                # Extract the text inside the button or its parent
                color_name = await color_btn.inner_text()
                
                # If there are sizes, click through them too
                if size_buttons:
                    for size_btn in size_buttons:
                        await size_btn.click(force=True)
                        size_name = await size_btn.inner_text()
                        
                        # Amazon dynamically reloads the price via AJAX. We MUST wait.
                        await page.wait_for_timeout(1500) 
                        
                        results["variations"].append(await extract_price_and_stock(page, color_name, size_name))
                else:
                    # If it's just colors, no sizes
                    await page.wait_for_timeout(1500)
                    results["variations"].append(await extract_price_and_stock(page, color_name, "N/A"))

            print("Scraping complete!")
            return results
            
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            return None
            
        finally:
            print("Closing browser...")
            await browser.close()

# Helper function to grab the price and stock after a click
async def extract_price_and_stock(page, color_name, size_name):
    # Amazon stores the main price in a few different places depending on the layout. 
    # .a-price-whole is the most common for the main dollars.
    price_element = page.locator('.a-price-whole').first
    price_text = await price_element.inner_text() if await price_element.count() > 0 else "0"
    
    # Clean the price (e.g., "49." -> 49)
    price = int(''.join(filter(str.isdigit, price_text))) if any(char.isdigit() for char in price_text) else 0
    
    # Check Amazon's specific availability div
    stock_element = page.locator('#availability span').first
    stock_text = await stock_element.inner_text() if await stock_element.count() > 0 else "In Stock"
    availability = "Out of Stock" if "currently unavailable" in stock_text.lower() or "out of stock" in stock_text.lower() else "In Stock"
    
    print(f"Scraped: {color_name.strip()} - {size_name.strip()} | Price: ${price} | Status: {availability}")
    
    return {
        "color": color_name.strip('\n'),
        "size": size_name.strip('\n'),
        "price": price,
        "availability": availability
    }

if __name__ == "__main__":
    # A real Amazon URL for a men's t-shirt that has multiple colors and sizes
    amazon_url = "https://www.amazon.in/Sony-DualSense-Wireless-Controller-PlayStation/dp/B0BMPLHLZ9/ref=asc_df_B0BMPLHLZ9?mcid=fd77df7f36a235a4baf4c9d540cd57a6&tag=googleshopdes-21&linkCode=df0&hvadid=709856235297&hvpos=&hvnetw=g&hvrand=14374969518283411509&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9061992&hvtargid=pla-1918381446187&psc=1&hvocijid=14374969518283411509-B0BMPLHLZ9-&hvexpln=0&gad_source=1" 
    
    # Run the asynchronous scraper
    data = asyncio.run(scrape_amazon_product(amazon_url))
    
    if data:
        print("\n--- FINAL JSON OUTPUT ---")
        print(json.dumps(data, indent=4))