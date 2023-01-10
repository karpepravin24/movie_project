# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import file_operations as fo


def find_latest_url():
    # Create a new Chrome browser instance with the "--headless" option,
    # which allows the browser to run in the background without opening a window.

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the Google homepage and enter the search term "Vegamovies" into the search input field.
    driver.get('https://www.google.com/')
    input_box = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    input_box.send_keys("Vegamovies")
    input_box.send_keys(Keys.ENTER)

    # Wait for the search results to load and then click on the first result.
    WebDriverWait(driver, 10)
    driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div[1]/a/h3').click()

    # Wait for an element on the resulting page to load and then extract the current URL of the page
    # and the URL of a link on the page.

    WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/div[2]/div/div')))
    vegamovies_url = driver.current_url
    dotmovies_url = driver.find_element(By.XPATH, '//*[@id="header-social"]/a[1]').get_attribute('href')

    print("Latest URL of Vegamovies & Dotmovies fetched successfully")
    # Return both URLs as a tuple.
    return vegamovies_url, dotmovies_url



if __name__ == "__main__":
    vegamovies_url, dotmovies_url = find_latest_url()
    fo.dump_latest_url(vegamovies_url=vegamovies_url, dotmovies_url=dotmovies_url, json_file_path="url_domain_names.json")

