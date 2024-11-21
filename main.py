from splinter import Browser
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import time
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

my_service = Service(executable_path='./msedgedriver.exe')
edge_options = Options()
browser = Browser('edge', service=my_service, options=edge_options)
base_url = "https://www.facebook.com/marketplace/112763262068685/propertyrentals/?"

# Enter credentials
phone_number = "" 
password = ""

location = 'Waterloo, ON'

# Search Parameters
minPrice = 100
maxPrice = 1300
daysSinceListed = 7
exact = False

url_addon = f"{base_url}minPrice={minPrice}&maxPrice={maxPrice}&daysSinceListed={daysSinceListed}&exact={exact}"

browser.visit(url_addon)

def find_element(driver, primary_locator, fallback_locator):
    try:
        return WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(primary_locator)
        )
    except:
        return WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(fallback_locator)
        )
'''
if browser.is_element_present_by_css('div[aria-label="Close"]', wait_time=10):
    # Click on the element once it's found
    browser.find_by_css('div[aria-label="Close"]').first.click()
'''
# Locate and fill the phone number and password fields using CSS selectors
# Wait for the email input field to be visible and interactable
# Use explicit wait to find and interact with elements by ID
email_input = WebDriverWait(browser.driver, 10).until(
    EC.element_to_be_clickable((By.ID, ":r1m:"))
)
email_input.send_keys(phone_number)

# Wait for the password input field to be visible and interactable
password_input = WebDriverWait(browser.driver, 10).until(
    EC.element_to_be_clickable((By.ID, ":r1p:"))
)
password_input.send_keys(password)

# Click the login button
login_button = WebDriverWait(browser.driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Accessible login button"]'))
)
login_button.click()

# Wait for the Marketplace page to load
time.sleep(5)

# Ensure the page is interactable by clicking somewhere
WebDriverWait(browser.driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'body'))).click()

scroll_count = 20
scroll_delay = 5
last_height = browser.execute_script("return document.body.scrollHeight")

for _ in range(scroll_count):    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(scroll_delay)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html = browser.html
market_soup = soup(html, 'html.parser')
browser.quit()

titles_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
titles_list = [title.text.strip() for title in titles_div]

# Extracting Prices
prices_div = market_soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
prices_list = [price.text.strip() for price in prices_div if 'CA$' in price.text]  # Filter only price-like values

# Extracting Locations
locations_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84")
locations_list = [location.text.strip() for location in locations_div if re.match(r'(\w+(?:-\w+)?, [A-Z]{2})', location.text)]  # Filter valid location text

urls_div = market_soup.find_all('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv")
urls_list = [url.get('href') for url in urls_div]

'''
print("Titles:", titles_list)
print(len(titles_list))
print("Prices:", prices_list)
print(len(prices_list))
print("Locations:", locations_list)
print(len(locations_list))
#print("URLs:", urls_list)
print(len(urls_list))
'''

properties_list = []

# Check if all lists have the same length
min_len = min(len(titles_list), len(prices_list), len(locations_list))

# Loop through and append data to the dictionary
properties_list = []

for i in range(min_len):
    properties_dict = {}
    properties_dict["Title"] = titles_list[i]
    properties_dict["Price"] = int(re.sub(r'[^\d]','', prices_list[i])) 
    properties_dict["Location"] = locations_list[i]
    properties_dict["Link"] = "https://www.facebook.com" + urls_list[i] 
    properties_list.append(properties_dict)

'''
print(properties_list)
'''

properties_df = pd.DataFrame(properties_list)
csv_file_path = r'C:\Users\abc\Desktop\FB-WebScraper\raw_data.csv'
properties_df.to_csv(csv_file_path, index=True)

# Filter through to get only properties for chosen location
filtered_df = properties_df[properties_df['Location'].str.lower() == location.lower()]

'''
print(filtered_df)
'''

csv_file_path = r'C:\Users\abc\Desktop\FB-WebScraper\filtered_data.csv'
filtered_df.to_csv(csv_file_path, index=True)
