from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    options = Options()
    # we use the browser in headless mode, this can be useful if we run the script on a dedicated server
    # or if we just want to avoid popping a window on our computer
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.lemonde.fr/")
    # make sure to manage the case where it fails, to avoid getting multiple browser running in the bg of your machine
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.Live__center')))
        live_banner_html = element.get_attribute(("innerHTML"))
        if live_banner_html == None:
            raise Exception("absent-live-banner")
        banner_elements = BeautifulSoup(live_banner_html, "html.parser").find_all(
            "li", class_="New")
        if len(banner_elements) == 0:
            raise Exception("absent-live-banner-elements")
        for element in banner_elements:
            title = element.find("div", class_="New__content").get_text()
            time = element.find("div", class_="New__time").get_text()
            print("{}, {}".format(time, title))

        # now, navigate to the main page of wikipedia, do a search and take a screenshot of the result
        driver.get("https://en.wikipedia.org/wiki/Main_Page")
        input_box = driver.find_element(By.NAME, "search")
        input_box.send_keys("chirality")

        # to avoid the stale element exception, it is recommended to relocate the element after it has been used
        # see: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/#stale-element-reference-exception
        input_box = driver.find_element(By.NAME, "search")
        input_box.send_keys(Keys.RETURN)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'firstHeading')))
        driver.save_screenshot("./search-result.png")

    except Exception as e:
        print(e)
        driver.close()

    driver.close()
