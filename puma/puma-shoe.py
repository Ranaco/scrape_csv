from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By


def get_shoe():
    url = "https://in.puma.com/in/en/pd/mayze-crashed-prm-womens-sneakers/393070?swatch=03&referrer-category=womens"

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(url)

    wait = WebDriverWait(driver, 10)

    color_grid_div = wait.until(EC.presence_of_element_located(
        (
            By.CSS_SELECTOR, ".grid.gap-1"
        )))
    color_div_list = color_grid_div.find_elements(By.TAG_NAME, "label")

    shoe_info = {}

    for color in color_div_list:

        color.click()
        time.sleep(1)

        title_h1 = wait.until(EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".tw-19nnhf.tw-lxvy65.tw-ou8532.tw-p9uz4a.tw-1h4nwdw"
            )))
        org_price_div = wait.until(EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                '[data-test-id="item-sale-price-pdp"]'
            )))
        discounted_price_div = wait.until(EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                '.whitespace-nowrap.text-base.line-through.opacity-50.override\\:font-bold.override\\:opacity-100'
            )))

        size_div_list = wait.until(EC.presence_of_all_elements_located(
            (
                By.CSS_SELECTOR,
                ".relative.border.flex.items-center.justify-center.flex-none.rounded-sm.cursor-pointer"
            )))
        product_code_parent_div = wait.until(EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".tw-1h4nwdw.tw-p9uz4a.tw-xwzea6.list-disc.list-inside"
            )))

        product_code_div = product_code_parent_div.find_element(
            By.TAG_NAME, "li"
        )
        category = "Men" if "Men" in title_h1.text else "Women" if "Women" in title_h1.text else "Unisex"

        shoe_info['title'] = title_h1.text
        shoe_info['org_price'] = org_price_div.text
        shoe_info['discounted_price'] = discounted_price_div.text
        shoe_info['size'] = [size.text for size in size_div_list]
        shoe_info['product_code'] = product_code_div.text.replace(
            "Style:", "").strip()
        shoe_info['category'] = category

        print(shoe_info)


get_shoe()
