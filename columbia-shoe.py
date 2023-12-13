from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://columbiasportswear.co.in/men/footwear-men/columbia-men-grey-crestwood-waterproof-bm5372-053"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get(url)

color_list_div = driver.find_element(By.CLASS_NAME, "grop-product-product")
color_list = color_list_div.find_elements(By.TAG_NAME, "a")

color_urls = []

for color_div in color_list:
    url = color_div.get_attribute("href")
    color_urls.append(url)

colors_info = []

for i in range(len(color_urls)):
    color_info = {
        "color_name": any,
        "product_info": {}
    }
    try:
        color_info = {
            "color_name": color_list[i].get_attribute('data-color'),
            "product_info": {}
        }

    except StaleElementReferenceException:
        pass

    driver.get(color_urls[i])

    wait = WebDriverWait(driver, 10)

    title_div = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "product-title")))
    dis_price_div = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "price-new")))
    org_price_div = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "price-old")))
    size_div_parent = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "option-main")))
    size_div_list = size_div_parent.find_elements(By.TAG_NAME, "div")
    review_div = wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "review_total")))
    star_count_div = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "actual-star")))
    data_col_div = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "col-sm-5")))
    product_code_div = data_col_div.find_element(By.TAG_NAME, "p")

    color_info["product_info"]["title"] = title_div.text
    color_info["product_info"]["dis_price"] = dis_price_div.text
    color_info["product_info"]["org_price"] = org_price_div.text
    color_info["product_info"]["size"] = size_div_list[0].text.strip()
    color_info["product_info"]["star_count"] = star_count_div.text[0]
    color_info["product_info"]["product_code"] = product_code_div.text.replace(
        "SKU :", "").strip()

    colors_info.append(color_info)

# Print the collected information for each color
for color_info in colors_info:
    print(f"Color: {color_info['color_name']}")
    print(f"Title: {color_info['product_info']['title']}")
    print(f"Discounted Price: {color_info['product_info']['dis_price']}")
    print(f"Original Price: {color_info['product_info']['org_price']}")
    print(f"Size: {color_info['product_info']['size']}")
    print(f"Star Count: {color_info['product_info']['star_count']}")
    print(f"Product Code: {color_info['product_info']['product_code']}")
    print("\n")

driver.quit()
