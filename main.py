import requests
from bs4 import BeautifulSoup
import pandas as pd
import file_operations as fo
import telegram_operations as to


def scrape_page(url, last_run_list):
    """
    Scrape data from a webpage and return a Pandas dataframe with the scraped data.

    Parameters:
        url (str): The URL of the webpage to be scraped.
        last_run_list (list): A list of movie names from a previous run of the function.

    Returns:
        df (pandas.DataFrame): A Pandas dataframe containing the scraped data.
        movie_fullname_list (list): A list of the full movie names from the scraped data.
    """

    # Initialize lists to store scraped data and full movie names
    values_list = []
    movie_fullname_list = []

    # Set up a counter variable and a loop to scrape multiple pages
    i = 1
    while i < 3:
        # Make an HTTP GET request to the specified URL
        page = requests.get(url, timeout=20)

        # If the request is successful (status code is 200)
        if page.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(page.text, 'lxml')

            # Extract all movie articles from the page
            articles = soup.find_all('article')

            # Iterate over each movie article
            for article in articles:
                # Extract the full movie name and link from the article
                full_name = article.find('h3', class_='entry-title h5 h6-mobile post-title').text[10:].strip()
                link_box = article.find('h3', class_='entry-title h5 h6-mobile post-title')
                link = link_box.find('a').get('href').strip()

                # Extract the image link from the article
                image_link = article.find('img').get('src')

                # Split the full movie name into the title and year
                movie_list = full_name.split('(')
                title = movie_list[0].strip()

                # Store the extracted information in a list
                scraped_list = [full_name, title, link, image_link]

                # Append the full movie name to the movie_fullname_list
                movie_fullname_list.append(full_name)

                # If the movie's full name is not in the last_run_list, append the scraped_list to the values_list
                if full_name not in last_run_list:
                    values_list.append(scraped_list)

        # If the request was not successful, skip the rest of the loop iteration
        else:
            continue

        # Increment the counter and update the URL for the next iteration
        i += 1
        url = url + f"page/{i}/"

    # Create a Pandas dataframe from the values_list
    df = pd.DataFrame(values_list, columns=['full_name', 'title', 'link', 'image_link'])

    return df, movie_fullname_list


if __name__ == "__main__":
    # Get the updated URLs from the JSON file
    latest_url_dictionary = fo.get_updated_url(json_file_path = 'url_domain_names.json')
    # Extract the URLs for the 'vegamovies' and 'dotmovies' domains
    vegamovies_url        = latest_url_dictionary['vegamovies_url']
    dotmovies_url         = latest_url_dictionary['dotmovies_url']

    # Get the lists of movies from the last run of the script for each domain
    vegamovies_last_run_list = fo.get_last_run_results(domain = 'vegamovies')
    dotmovies_last_run_list  = fo.get_last_run_results(domain ='dotmovies')

    # Scrape the data from the 'vegamovies' and 'dotmovies' webpages
    vegamovies_df, vegamovies_full_title_list = scrape_page(url = vegamovies_url,
                                                            last_run_list = vegamovies_last_run_list)
    dotmovies_df, dotmovies_full_title_list = scrape_page(url = dotmovies_url,
                                                          last_run_list = dotmovies_last_run_list)

    # Saving current run values to json file
    fo.dump_latest_run_results(domain='vegamovies', dataframe=vegamovies_df)
    fo.dump_latest_run_results(domain='dotmovies', dataframe=dotmovies_df)

    # Sending data to telegram channel
    to.send_to_telegram(channel = 'bollywood', dataframe = dotmovies_df,
                        chat_id = os.environ['BOOLYWOOD_CHAT_ID'], telegram_token = os.environ['TELEGRAM_TOKEN'])
    to.send_to_telegram(channel = 'bollywood', dataframe = dotmovies_df,
                        chat_id = os.environ['HOOLYWOOD_CHAT_ID'], telegram_token = os.environ['TELEGRAM_TOKEN'])


