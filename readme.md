# Facebook Marketplace Scraper

This project scrapes Facebook Marketplace listings based on certain parameters (price, location, days since listed) and outputs the data in CSV format for further analysis.

## **Overview**
This scraper automates the process of collecting property rental listings from Facebook Marketplace. The script logs in to Facebook, navigates to the Marketplace property rentals section, and scrapes data such as title, price, location, and listing URL. The data is then filtered by a specified location and saved to two CSV files: one with all listings and one with the filtered results.

## **Components**

### **1. Main Script (`main.py`)**
The `main.py` script is responsible for the scraping process:
- **Initial Setup:**
  - **Selenium and Splinter:** These libraries are used to automate browser actions, including logging into Facebook, scrolling through the listings, and interacting with the page.
  - **WebDriver and Browser Initialization:** Configures the Edge browser and ensures that the page loads correctly.
- **Scraping Logic:**
  - The script navigates to the Marketplace property rentals section with configurable search parameters (price range, days since listed, and location).
  - **Data Extraction:** Extracts the listing's title, price, location, and URL using BeautifulSoup.
  - **Filtering:** After scraping, the data is filtered based on a specific location (e.g., 'Waterloo, ON').
  - **Saving Results:** The scraped data is saved into CSV files for further analysis.

### **2. Web Scraping Workflow**
The script follows these main steps:
1. **Browser Setup:** It uses Selenium with Edge WebDriver for browsing automation, ensuring the page is loaded and interactable.
2. **Login:** The script logs into Facebook using the provided credentials (phone number and password).
3. **Page Interaction:**
   - Scrolls through the listings to load more items dynamically.
   - Extracts relevant information from each listing (title, price, location, and URL).
4. **Data Extraction:**
   - Scrapes the data using BeautifulSoup.
   - Filters out listings based on the defined price range, location, and days since the listing.
5. **Save to CSV:**
   - The data is saved to a CSV file in two versions:
     - **Raw Data:** Contains all scraped listings.
     - **Filtered Data:** Contains listings specific to the chosen location.

### **3. Libraries and Dependencies**
The script requires the following libraries:
- **Splinter:** For browser automation.
- **BeautifulSoup:** For parsing HTML and extracting data.
- **Selenium:** For controlling the browser and interacting with dynamic web elements.
- **Pandas:** For storing and manipulating the scraped data.
- **Regular Expressions (`re`):** For cleaning and formatting extracted data.
