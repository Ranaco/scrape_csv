from pandas.core.dtypes.dtypes import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

from selenium.webdriver.common.by import By


def get_shoe_data():

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://www.adidas.co.in/galaxy-6-shoes/GW3848.html")

    color_list_div = driver.find_element(
        By.CLASS_NAME, "color-chooser-grid___1ZBx_"
    )

    color_list = []

    try:
        color_list = color_list_div.find_elements(By.TAG_NAME, "a")
    except NoSuchElementException:
        print("No colors available")

    color_urls = []

    if len(color_list) != 0:
        for color in color_list:
            url = color.get_attribute('href')
            color_urls.append(url)
    else:
        color_urls = ["https://www.adidas.co.in/galaxy-6-shoes/GW3848.html"]

    print(color_urls)

    for i in range(len(color_urls)):

        driver.get(color_urls[i])

        check = False

        if len(color_urls) > 1:
            try:
                account_div = driver.find_element(
                    By.CLASS_NAME, "gl-modal__close")
                print(account_div, "account_div")
                account_div.click()
            except Exception:
                print("No account")

            check = True

        wait = WebDriverWait(driver, 10)

        shoe_data = {}
        if check is True:

            # size_list_div = wait.until(
            #     EC.presence_of_all_elements_located(
            #         (
            #             By.CSS_SELECTOR, ".gl-label.size___2lbev"
            #         )))
            title_div = wait.until(EC.presence_of_all_elements_located((
                By.CLASS_NAME,
                "name___120FN"
            )))[1]
            discount_price_div = wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, ".gl-price-item.gl-price-item--sale.notranslate"
            )))[1]

            original_price_div = wait.until(
                EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR, ".gl-price-item.gl-price-item--crossed.notranslate"
                )))[1]
            star_rate_div = wait.until(
                EC.presence_of_element_located((
                    By.CLASS_NAME, "ratings-label-container___13pr-"
                )))
            review_div = wait.until(
                EC.presence_of_all_elements_located((
                    By.CLASS_NAME, "accordion-title___2sTgR"
                )))[2]
            details_button = wait.until(EC.presence_of_element_located((
                By.CLASS_NAME, "accordion__header___3Pii5"
            )))
            #
            description_button_list = wait.until(EC.presence_of_all_elements_located((
                By.CLASS_NAME, "accordion__header___3Pii5"
            )))
            detail_button = description_button_list[1]
            driver.execute_script(
                'arguments[0].scrollIntoView();', details_button)

            detail_button.click()

            product_code_div_main = wait.until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "gl-vspace-bpall-small")))
            product_code_div = None
            for product in product_code_div_main:
                if "Product code:" in product.text:
                    product_code_div = product
            comfort_code_div = wait.until(EC.presence_of_all_elements_located((
                By.CLASS_NAME, "gl-vspace-bpall-small"
            )))[0]

            shoe_data['title'] = title_div.text
            shoe_data['discount_price'] = discount_price_div.text
            shoe_data['original_price'] = original_price_div.text
            shoe_data['star_rate'] = star_rate_div.text
            shoe_data['review_count'] = re.findall(r'\d+', review_div.text)[0]
            shoe_data['product_code'] = product_code_div.text.replace(
                "Product code:", "").strip()
            shoe_data['comfort'] = comfort_code_div.text
            print(shoe_data)


get_shoe_data()
