from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_shoe_data():

    # Creates Chrome WebDriver instance.
    driver = webdriver.Chrome()

    # Let's maximize the automated chrome window
    driver.maximize_window()

    # Navigate to shine website
    driver.get("https://www.adidas.co.in/men%7Cunisex%7Cwomen-shoes")

    # Wait for the page to load
    time.sleep(3)

    # Imports the HTML of the webpage into python
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    shoe_links = []

    while True:
        # Grabs the HTML of each product
        product_card = soup.find_all(
            'div', class_='glass-product-card color-variations__fixed-size plp-product-card___2Tf-5 product-card-content___3R3aL lift-image___3FzoX')

        # Grabs the product details for every product on the page and adds each product as a row in our dataframe
        for product in product_card:
            try:
                link = "https://adidas.co.in" + product.find(
                    'a', class_='glass-product-card__assets-link').get('href')
                # shoe_links.append('https://www.adidas.co.in' + link)
                driver.get(link)
                shoe_soup = BeautifulSoup(driver.page_source, 'html.parser')
                title_div = shoe_soup.find("h1", {"class": "name___120FN"})

            except Exception as e:
                # print(f"Error processing product {idx}: {e}")
                print("Some error fetching shoe link", e)

        # Check for the presence of the next page lin print("Some error fetching shoe link")k
        next_page = soup.find('a', {'data-auto-id': 'plp-pagination-next'})
        if not next_page:
            break

    # Navigate to the next page
        next_page_full = 'https://www.adidas.co.in' + next_page.get('href')
        driver.get(next_page_full)
    # time.sleep(1)  # Add a delay to ensure the page loads

    # Imports the HTML of the webpage into python
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    # # Create a DataFrame
    # df = pd.DataFrame(shoe_links)
    #
    # # Save DataFrame to CSV
    # df.to_csv("adidas_links_data_part_1.csv", index=False)


get_shoe_data()

# # Create a DataFrame
# df = pd.DataFrame(shoe_links)
#
# # Save DataFrame to CSV
# df.to_csv("adidas_links_data_part_1.csv", index=False)

# Close the Chrome WebDriver
