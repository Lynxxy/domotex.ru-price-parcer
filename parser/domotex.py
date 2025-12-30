import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def parse_price(url: str) -> int | None:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(3)

    try:
        price_element = driver.find_element(
            By.CSS_SELECTOR,
            "span.price_value"
        )

        price_text = price_element.get_attribute("textContent")
        price_text = price_text.replace("\xa0", "").strip()

        price = int(price_text)
        return price

    except Exception as e:
        print("Parse error:", e)
        return None
    finally:
        driver.quit()

def parse_name(url: str) -> str | None:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(3)

    try:
        name_element = driver.find_element(
            By.CSS_SELECTOR,
            "h1"
        )
        return name_element.text.strip()
    except Exception:
        return None
    finally:
        driver.quit()



if __name__ == "__main__":
    test_url = "https://www.domotex.ru/catalog/mebel_dlya_vannykh_komnat/modul_podvesnoy_akvaton_oliviya_grey_dub_oyster_pravyy_1a254703olugr/"
    print(parse_price(test_url))
