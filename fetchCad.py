#This script automates the process of web scraping product details and downloading CAD files from the McMaster-Carr website.
#It utilizes Selenium with a Chrome WebDriver to access product pages based on a list of part numbers read from a CSV file.
#For each part number, the script does the following:
#1. Creates a unique folder for the part's files.
#2. Downloads product details such as the name and specifications from the web page.
#3. Attempts to download the CAD file associated with the part, if available.
#4. Saves all data into the corresponding part's folder.

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from selenium_stealth import stealth

# Load product numbers from CSV
file_path = r'PartNumbers.csv'
part_numbers_df = pd.read_csv(file_path)
part_numbers = part_numbers_df['Part Number'].tolist()

# Set up Chrome WebDriver with custom download folder settings
chrome_options = webdriver.ChromeOptions()

# Base directory for part-specific folders
base_output_dir = r'\scrape-mcmaster-master\part_files'

# Set default download directory
prefs = {
    "download.default_directory": base_output_dir,
    "download.prompt_for_download": False,  # Disable download prompt
    "directory_upgrade": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Set up WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# Base URL
base_url = "https://www.mcmaster.com/"

# Iterate over the product numbers
for product_number in part_numbers:
    try:
        # Create directory for this product number
        part_dir = os.path.join(base_output_dir, product_number)
        os.makedirs(part_dir, exist_ok=True)

        # Update download directory for this product number
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": part_dir
        })

        # Construct the URL for each product
        url = f"{base_url}{product_number}/"

        # Open the product page
        driver.get(url)

        # Wait for the page to load properly
        time.sleep(5)  # Adjust as needed based on page load time

        # Scraping the product name and specifications, and saving them to a text file
        text_file_path = os.path.join(part_dir, f'{product_number}_details.txt')
        with open(text_file_path, 'w') as file:
            # Scraping the product name
            try:
                product_name = driver.find_element(By.TAG_NAME, 'h1').text
                print(f"Product Name: {product_name}")
                file.write(f"Product Number: {product_number}\n")
                file.write(f"Product Name: {product_name}\n")
            except Exception as e:
                print(f"Error finding the product name: {e}")
                file.write(f"Error finding the product name: {e}\n")

            # Scraping the specifications
            try:
                # Find the table by class name
                specs_table = driver.find_element(By.CLASS_NAME, "ProductDetailTable_product-detail-spec-table__3T6Yi")

                # Find all rows within the table
                specs_rows = specs_table.find_elements(By.TAG_NAME, 'tr')

                # Extract spec names and values from each row
                for row in specs_rows:
                    spec_name = row.find_element(By.CLASS_NAME, "ProductDetailRow_product-detail-spec-row-label__1zkIK").text.strip()
                    spec_value = row.find_element(By.CLASS_NAME, "ProductDetailRow_product-detail-spec-row-value__3zb69").text.strip()
                    #print(f"{spec_name}: {spec_value}")
                    file.write(f"{spec_name}: {spec_value}\n")
                file.write("\n")
            except Exception as e:
                print(f"Error finding the specifications: {e}")
                file.write(f"Error finding the specifications: {e}\n\n")

        # Locate and download the CAD file for this product (if available)
        try:
            download_button = driver.find_element(By.LINK_TEXT, "Download")
            download_button.click()

            # Wait for the CAD file to be downloaded
            time.sleep(10)  # Adjust based on download time
            print(f"CAD download initiated for {product_number}.")
        except Exception as e:
            print(f"Error locating or clicking the download button for {product_number}: {e}")

    except Exception as e:
        print(f"Failed to load page for {product_number}: {e}")

# Close the browser after all operations
driver.quit()

print(f"Product details and CAD files saved in {base_output_dir}")
