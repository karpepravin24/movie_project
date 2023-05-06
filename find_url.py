# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import requests
from bs4 import BeautifulSoup

import file_operations as fo


def get_headless_driver():
    # # Create a new Chrome browser instance with the "--headless" option,
    # # which allows the browser to run in the background without opening a window.
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def check_url_syntax(url):
    if not url.endswith("/"):
        valid_url = url = "/"
        return valid_url
    else:
        return url

def get_vegamovies_url():

    driver = get_headless_driver()

    # Navigate to the Google homepage and enter the search term "Vegamovies" into the search input field.
    driver.get('https://www.google.com/')
    input_box = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')
    input_box.send_keys("Vegamovies")
    input_box.send_keys(Keys.ENTER)

    # Wait for the search results to load and then click on the first result.
    WebDriverWait(driver, 15)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    first_search_result = soup.find('div', class_='MjjYud')
    vegamovies_url = first_search_result.find('a').get('href')
    vegamovies_url = check_url_syntax(vegamovies_url)
    driver.close()

    return vegamovies_url


def get_dotmovies_url(vegamovies_url):
    driver = get_headless_driver()
    driver.get(vegamovies_url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    header = soup.find('div', {"id":'header-social'})
    dotmovies_url = header.find('a').get('href')

    # dotmovies_url = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/a[1]').get_attribute('href')
    dotmovies_url = check_url_syntax(dotmovies_url)
    driver.close()

    return dotmovies_url


if __name__ == "__main__":
    vegamovies_url = get_vegamovies_url()
    print("Vegamovies url:   ",vegamovies_url)
    dotmovies_url = get_dotmovies_url(vegamovies_url)
    print("Vegamovies URL:  ", vegamovies_url)
    print("Dotmovies URL :  ", dotmovies_url)

    fo.dump_latest_url(vegamovies_url=vegamovies_url, dotmovies_url=dotmovies_url,
                       json_file_path="url_domain_names.json")
