# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import file_operations as fo


def find_latest_url():
    # # Create a new Chrome browser instance with the "--headless" option,
    # # which allows the browser to run in the background without opening a window.
    #
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the Google homepage and enter the search term "Vegamovies" into the search input field.
    driver.get('https://www.google.com/')
    input_box = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    input_box.send_keys("Vegamovies")
    input_box.send_keys(Keys.ENTER)

    # Wait for the search results to load and then click on the first result.
    WebDriverWait(driver, 15)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    first_search_result = soup.find('div', class_ = 'MjjYud')
    vegamovies_url = first_search_result.find('a').get('href')
    print("Vegamovies_link:  ", vegamovies_url)

    page = requests.get(vegamovies_url, timeout = 20)
    soup = BeautifulSoup(page.text, 'lxml')
    header = soup.find('div', attrs={'id':'header-social'})
    dotmovies_url = header.find('a').get('href')
    print("Dotmovies_link:  ", dotmovies_url)

    print("Latest URL of Vegamovies & Dotmovies fetched successfully")
    # Return both URLs as a tuple.
    return vegamovies_url, dotmovies_url


if __name__ == "__main__":
    vegamovies_url, dotmovies_url = find_latest_url()
    fo.dump_latest_url(vegamovies_url=vegamovies_url, dotmovies_url=dotmovies_url, json_file_path="url_domain_names.json")

