import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 5)


def get_shoe(url):
    url = "https://www.adidas.co.in/superstar-shoes/EG4958.html"
    driver.get(url)

    color_link_list = []
    color_list = []
    try:
        color_link_parent = wait.until(EC.presence_of_element_located((
            By.CLASS_NAME, "color-chooser-grid___1ZBx_"
        )))

        color_link_div_list = color_link_parent.find_elements(
            By.TAG_NAME, "a"
        )

        color_link_list = []

        for color in color_link_div_list:
            href = color.get_attribute("href")
            color_value = color.find_element(
                By.TAG_NAME, 'img').get_attribute("alt") or ""
            color_list.append(color_value.replace("Colour:", "").strip())
            color_link_list.append(href)
    except Exception:
        color_link_list.append(url)
        print("No colors found")
    print(color_link_list)

    closed = False
    for i in range(len(color_link_list)):
        driver.get(color_link_list[i])

        shoe_data = {}

        if not closed:
            close_button_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CLASS_NAME, "gl-modal__close"
            )))
            close_button_div.click()
            closed = True

        if closed:
            shoe_name_div = driver.find_elements(
                By.CLASS_NAME, "name___120FN"
            )[1]

            shoe_type_div = driver.find_element(
                By.CSS_SELECTOR, "div[data-auto-id=product-category]"
            )

            price_div = driver.find_elements(
                By.CSS_SELECTOR, ".price-wrapper___2Pj9R.inline___297tt.price___35NVI.gl-flex-col"
            )[1]

            star_div = driver.find_element(
                By.CLASS_NAME, "ratings-label-container___13pr-"
            )

            accordian_list = wait.until(EC.presence_of_all_elements_located((
                By.CLASS_NAME, "accordion__header___3Pii5"
            )))

            details_div = None
            review_div = None
            product_code_div = None
            comfort_div = None
            size_div = None
            durability_div = None
            review_count = "NaN"

            try:
                for accordian in accordian_list:
                    if "Details" in accordian.text:
                        details_div = accordian
                        break
                for accordian in accordian_list:
                    if "Reviews" in accordian.text:
                        review_div = accordian
                        try:
                            review_count_div = accordian.find_element(
                                By.CLASS_NAME, "accordion-title___2sTgR"
                            )
                            review_count = re.findall(
                                r"\d+", review_count_div.text)[0]
                        except Exception:
                            print("No review count")
                        break
                # print(
                #     f"The values of both divs from accordian are {details_div} and {review_div}")
            except Exception:
                print("No accordians found")

            if details_div is not None:
                details_div.click()
                div_list = wait.until(EC.presence_of_all_elements_located((
                    By.CLASS_NAME, "gl-vspace-bpall-small"
                )))

                for div in div_list:
                    if "Product code" in div.text:
                        product_code_div = div
                        # print(product_code_div.text)
                        break

            if review_div is not None:
                review_div.click()
                try:
                    slider_div_list = wait.until(EC.presence_of_all_elements_located((
                        By.CLASS_NAME, "gl-comparison-bar__indicator"
                    )))
                    comfort_div = slider_div_list[0]
                    durability_div = slider_div_list[1]
                    size_div = slider_div_list[2]
                except Exception:
                    print("No review data found")

            shoe_data['shoe_name'] = shoe_name_div.text
            shoe_data['price'] = price_div.find_element(By.TAG_NAME,
                                                        "div").text.replace(
                "₹", "").strip()
            shoe_data['star'] = star_div.text
            shoe_data['shoe_type'] = shoe_type_div.text.split("•")[0] if len(
                shoe_type_div.text.split("•")) == 1 else shoe_type_div.text.split("•")[1]
            shoe_data['size_count'] = "NaN"
            shoe_data['comfort'] = re.findall(r'\d+',
                                              comfort_div.get_attribute("style"))[0] if comfort_div is not None else "NaN"
            shoe_data['durability'] = re.findall(r'\d+',
                                                 durability_div.get_attribute("style"))[0] if durability_div is not None else "NaN"
            shoe_data['size'] = re.findall(r'\d+',
                                           size_div.get_attribute("style"))[0] if size_div is not None else "NaN"
            shoe_data['review_count'] = review_count
            shoe_data['url'] = url
            shoe_data['color_count'] = len(color_list)
            shoe_data['product_code'] = product_code_div.text.replace(
                "Product code:", "").strip()
            shoe_data['brand'] = "adidas"

            data_table = {
                'shoe_name': shoe_data['shoe_name'],
                'org_price': shoe_data['price'],
                # 'discounted_price': shoe_data['discounted_price'],
                'url': shoe_data['url'],
                'category': shoe_data['shoe_type'].strip(),
                'review_count': shoe_data['review_count'],
                'star': shoe_data['star'],
                'product_code': shoe_data['product_code'],
                'shoe_type': shoe_data['shoe_type'],
                'durability': shoe_data['durability'],
                'comfort': shoe_data['comfort'],
                'size': shoe_data['size'],
                'size_count': shoe_data['size_count'],
                'color_count': shoe_data['color_count'],
                'brand': shoe_data['brand'],
            }

            print(data_table)


get_shoe("")

