from pandas.core.dtypes.dtypes import re
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

from selenium.webdriver.common.by import By


def get_puma_shoes():
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = "https://in.puma.com/in/en/mens/mens-shoes"

    driver.get(url)

    item_count_div = driver.find_element(
        By.CSS_SELECTOR, ".uppercase.font-bold.text-lg.md\\:text-xl")
    item_count = re.findall(r'\d+', item_count_div.text)
    for i in range(int(item_count[0]) // 24):
        time.sleep(1)
        link_div_list = driver.find_elements(
            By.CLASS_NAME, "relative w-full flex flex-col gap-2"
        )


get_puma_shoes()
