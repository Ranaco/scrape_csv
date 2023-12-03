from bs4 import BeautifulSoup
# import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# Importing required Exceptions which needs to handled
# from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException
import time
import warnings
warnings.filterwarnings('ignore')


# Table 1 : Name, category, no. of colors, price
# Table 2 : Count of sizes, colors 1, 2, 3, 4, 5, Style Code/Product details
# Table 3: Reviews, Size, Comfort, durability /quality/
# performance(quantification), star rating,


def scrape_shoe_details(url, category):

    # Loop for table 3

    # Creates Chrome WebDriver instance.
    driver = webdriver.Chrome()

    # Let's maximize the automated chrome window
    driver.maximize_window()

    # Navigate the Goole Map Website
    time.sleep(1)

    driver.get(url)
    tiles = driver.find_elements(
        By.CLASS_NAME, r'product-card__body')

    for i in range(len(tiles)):

        tiles[i].click()

        drop_down_list = driver.find_elements(By.CLASS_NAME, "css-1hbr3d8")

        for drop_down in drop_down_list:

            if "Size" in drop_down.text:
                size_div = drop_down.find_element(
                    By.CLASS_NAME, "css-u1dbz9")
                print(size_div.text)

            # raw_size = size_div.find_element(By.TAG_NAME, "li").text
            # print(raw_size)
            # if "Reviews" in drop_down.text:
            #     details_div = drop_down.find_element(
            #         By.CLASS_NAME, "css-rptnlm")
            #     star_div = details_div.find_element(By.TAG_NAME, "div")
            #     stars = star_div.get_attribute('aria-label')

            # ul_div = navbar_div.find_element(
            #     By.CLASS_NAME, "tt-o-page-list")
            #
            # page_count = len(ul_div.find_elements(
            #     By.TAG_NAME, "li"
            # ))
            # print(page_count)

            # review_content = review_parent_div.find_element(
            #     By.CLASS_NAME, "tt-c-reviews-list__content")

        driver.back()
        tiles = driver.find_elements(By.CLASS_NAME, r'product-card__body')

    # Loop for table 2
    # # Creates Chrome WebDriver instance.
    # driver = webdriver.Chrome()
    #
    # # Let's maximize the automated chrome window
    # driver.maximize_window()
    #
    # # Navigate the Goole Map Website
    # time.sleep(1)
    #
    # driver.get(url)
    # tiles = driver.find_elements(
    #     By.CLASS_NAME, r'product-card__body')
    #
    # for i in range(len(tiles)):
    #     tiles[i].click()
    #
    #     color_div_list = driver.find_elements(
    #         By.CLASS_NAME, r'css-b8rwz8')
    #
    #     for color_div in color_div_list:
    #         page_source = driver.page_source
    #         soup = BeautifulSoup(page_source, "html.parser")
    #         img = color_div.find_element(By.TAG_NAME, "img")
    #         color_name = str(img.get_attribute('alt')).split("/")
    #         color_div.click()
    #         size_count = len(driver.find_elements(
    #             By.CLASS_NAME, r'css-xf3ahq'))
    #         style_code = soup.find(
    #             "li", {"class": 'description-preview__style-color ncss-li'})
    #
    #         title = soup.find("h1", {"id": "pdp_product_title"})
    #         print(title.text if title is not None else "", "\n\n")
    #         print(category, " ", color_name, " ", str(size_count), " ",
    #               style_code.text.replace("Style: ", "")
    #               if style_code is not None else "", "\n")
    #
    #     driver.back()
    #     # Rehydrating tiles to check StaleElementReferenceException
    #     tiles = driver.find_elements(By.CLASS_NAME, r'product-card__body')
    #
    # Loop for Table 1
    # page_source = driver.page_source
    # soup = BeautifulSoup(page_source, 'html.parser')
    #
    # shoe_tile = soup.find_all('div', {"class": "product-card__body"})

    # for shoe in shoe_tile:
    #     detail_box = None
    #     detail_box = shoe.find(
    #         'div', {"class": "product-card__info disable-animations"})
    #     # handle when this class is not found
    #     if detail_box is None:
    #         detail_box = shoe.find(
    #             "div", {
    #                 "class":
    #                 "product-card__info disable-animations for--product"
    #             })
    #
    #     if detail_box is not None:
    #         name_div = detail_box.find(
    #             "div", {"class": "product-card__title"})
    #         color_div = detail_box.find(
    #             "div", {"class": "product-card__product-count"})
    #         price_div = detail_box.find(
    #             "div", {"class": "product-card__price"})
    #
    #         name = name_div.text.split()
    #         color = color_div.text.strip()[0]
    #         price = price_div.text.strip().replace("MRP : ", "").replace("₹", "").strip()


url_cat = ["https://www.nike.com/in/w/mens-shoes-nik1zy7ok",
           "https://www.nike.com/in/w/womens-shoes-5e1x6zy7ok"]

for url in url_cat:
    scrape_shoe_details(
        url, "men" if url_cat.index(url) == 0 else "women")
