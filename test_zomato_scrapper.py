import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# List of Zomato restaurant URLs
restaurant_links = [
    "https://www.zomato.com/kanpur"
    # Add more restaurant URLs as needed
]

# Initialize lists to store data
all_urls = []
all_rest_name = []
all_ratings = []
all_price = []
all_cuisine = []

# Set up Selenium WebDriver
driver = webdriver.Chrome()

for link in restaurant_links:
    driver.get(link)
    time.sleep(2)

    scroll_pause_time = 1.8
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    while True:
        driver.execute_script("window.scrollTo(0, {0});".format(screen_height * i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (screen_height) * i > scroll_height:
            break

    # Create a soup object
    soup = BeautifulSoup(driver.page_source, "html.parser")
    divs = soup.findAll('div', class_='jumbo-tracker')

    # Loop through restaurant divs and extract data
    restaurant_count = 0  # Counter to limit restaurants scraped

    for parent in divs:
        if restaurant_count >= 10:
            break  # Stop after scraping 10 restaurants

        name_tag = parent.find("h4")
        if name_tag is not None:  # Check if the tag exists
            rest_name = name_tag.text.strip()

            link_tag = parent.find("a")
            base = "https://www.zomato.com"
            link = urljoin(base, link_tag.get('href'))

            # Safely extract rating, price, and cuisine to avoid errors
            try:
                rating_tag = parent.div.a.next_sibling.div.div.div.div.div.div.div.text.strip()
            except AttributeError:
                rating_tag = None

            try:
                price_tag = parent.div.a.next_sibling.p.next_sibling.text.strip()
            except AttributeError:
                price_tag = None

            try:
                cuisine_tag = parent.div.a.next_sibling.p.text.strip()
            except AttributeError:
                cuisine_tag = None

            all_urls.append(link) 
            all_rest_name.append(rest_name)
            all_ratings.append(rating_tag)
            all_price.append(price_tag)
            all_cuisine.append(cuisine_tag)

            restaurant_count += 1  # Increment counter

# Create a DataFrame
df = pd.DataFrame({
    'links': all_urls,
    'names': all_rest_name,
    'ratings': all_ratings,
    'price for one': all_price,
    'cuisine': all_cuisine,
})

# Save restaurant data to a CSV file
df.to_csv("restaurant_data.csv", index=False)
print(df)

# Close the WebDriver
driver.close()
