from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import warnings
warnings.filterwarnings('ignore')


def scrape_addidas_shoes(url, category):
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(url)

    # Wait for the initial items to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "with-variation-carousel")))

    # # Scroll down to trigger loading more items
    # for _ in range(3):  # Adjust the number of scrolls based on your needs
    #     driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    #     time.sleep(2)  # Allow time for the items to load

    source = driver.page_source

    soup = BeautifulSoup(source, "html.parser")

    items = soup.find_all("div", {
                          "class": "glass-product-card color-variations__fixed-size plp-product-card___2Tf-5 product-card-content___3R3aL lift-image___3FzoX"})

    for item in items:
        # Your existing code to extract details
        title_div = item.find(
            "p", {"class": "glass-product-card__title"})
        price_div = None
        color_div = None

        try:
            price_div = item.find(
                "div", {"class": "gl-price-item gl-price-item--sale notranslate"})
        except NoSuchElementException:
            pass

        if not price_div:
            try:
                price_div = item.find(
                    "div", {"class": "gl-price-item notranslate"})

            except NoSuchElementException:
                pass

        try:
            color_div = item.find("span", {"class": "dark-grey___6ysQv"})
        except NoSuchElementException:
            pass

        title = title_div.text
        price = price_div.text if price_div else None
        color = color_div.text if color_div else "NA"
        print(title, price, color, category, "\n")

    driver.quit()


scrape_addidas_shoes("https://www.adidas.co.in/men-shoes", "men")
