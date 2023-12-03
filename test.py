
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import time
import warnings
warnings.filterwarnings('ignore')


def scrape_shoe_details(url, category):
    scraped_data = []

    # Creates Chrome WebDriver instance.
    driver = webdriver.Chrome()

    # Let's maximize the automated chrome window
    driver.maximize_window()

    # Navigate the Google Map Website
    time.sleep(1)

    driver.get(url)
    time.sleep(2)
    # Accept cookies
    try:
        cookie_accept_button = driver.find_element(
            By.XPATH, '//*[@id="hf_cookie_text_cookieAccept"]')
        cookie_accept_button.click()
    except ElementNotInteractableException:
        pass
    time.sleep(3)
    # Close popup
    try:
        popup_close_button = driver.find_element(
            By.XPATH, '//*[@id="gen-nav-commerce-header-v2"]/aside/div/div/div/div[1]/button')
        popup_close_button.click()
    except ElementNotInteractableException:
        pass

    tiles = driver.find_elements(By.CLASS_NAME, 'product-card__body')

    for i in range(len(tiles)):
        try:
            tiles[i].click()

            color_div_list = driver.find_elements(By.CLASS_NAME, 'css-b8rwz8')

            for color_div in color_div_list:
                try:
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")
                    img = color_div.find_element(By.TAG_NAME, "img")
                    color_name = str(img.get_attribute('alt')).split("/")

                    # Use ActionChains to move to the element before clicking
                    ActionChains(driver).move_to_element(
                        color_div).click(color_div).perform()

                    size_count = len(driver.find_elements(
                        By.CLASS_NAME, 'css-xf3ahq'))
                    style_code = soup.find(
                        "li", {"class": 'description-preview__style-color ncss-li'})

                    title = soup.find("h1", {"id": "pdp_product_title"})
                    data_entry = {
                        'title': title.text if title is not None else "",
                        'category': category,
                        'color_name': color_name,
                        'size_count': str(size_count),
                        'style_code': style_code.text.replace("Style: ", "") if style_code is not None else ""
                    }
                    scraped_data.append(data_entry)
                except StaleElementReferenceException:
                    # Handle StaleElementReferenceException by re-finding the element
                    continue
                except ElementClickInterceptedException:
                    # Handle ElementClickInterceptedException by moving to the element before clicking
                    ActionChains(driver).move_to_element(
                        color_div).click(color_div).perform()
                    continue

            driver.back()
            # Rehydrating tiles to check StaleElementReferenceException
            tiles = driver.find_elements(By.CLASS_NAME, 'product-card__body')
        except StaleElementReferenceException:
            # Handle StaleElementReferenceException by re-finding the element
            tiles = driver.find_elements(By.CLASS_NAME, 'product-card__body')
            continue

    driver.quit()
    return scraped_data


url_cat = ["https://www.nike.com/in/w/mens-shoes-nik1zy7ok",
           "https://www.nike.com/in/w/womens-shoes-5e1x6zy7ok"]

all_data = []

for url in url_cat:
    data = scrape_shoe_details(
        url, "men" if url_cat.index(url) == 0 else "women")
    all_data.extend(data)

# Now all_data contains the scraped information from both URLs
print(all_data)
