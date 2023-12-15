from selenium import webdriver
from pandas.core.dtypes.dtypes import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def get_links():

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    shoe_urls = []

    for url in urls:
        driver.get(url)
        item_count_div = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".wall-header__item_count"
        )))

        item_count = int(re.findall("\d+", item_count_div.text)[0])

        print(item_count)

        for i in range(item_count):
            # Scroll to the end of the page.
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            url_parent_div_list = wait.until(EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, "a[data-testid=product-card__link-overlay]"
            )))

            if i > 0:
                url_parent_div_list = url_parent_div_list[i:]

            url_element = url_parent_div_list[0]

            shoe_urls.append({"link": url_element.get_attribute("href")})

    driver.quit()
    df = pd.DataFrame(shoe_urls)
    df.to_csv("./nike-link.csv", index=False)


urls = ["https://www.nike.com/in/w/mens-shoes-nik1zy7ok",
        "https://www.nike.com/in/w/womens-shoes-5e1x6zy7ok"]

get_links()
