import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

import file_operations as fo


def shorten_url(url):
    # Hardcoded API token
    shrinkme_token = '888f858b84660d25a3aa34c2d50adc2ad6de73e4'

    try:
        # Send a GET request to the Shrinkme API endpoint, including the API token, the URL to be shortened, and the desired return format
        response = requests.get(f"https://shrinkme.io/api?api={shrinkme_token}&url={url}&format=text", timeout = 20)

        # Store the shortened URL returned by the API
        short_url = response.text

    except requests.exceptions.Timeout:
        print("Shortening API didn't responded, Timeout exception raised. Returned original URL")
        return url

    # Return the shortened URL if there is no timeout exception
    return short_url


def send_to_telegram(channel, dataframe, chat_id):
    """Sends a message to a Telegram channel with a description and image for each row in a dataframe.
    Arguments:
    channel -- the name of the Telegram channel to send the message to (either 'vegamovies' or 'dotmovies')
    dataframe -- a Pandas dataframe with columns 'title', 'full_name', 'image_link', and 'link'
    chat_id -- chat id of telegram channel in which mesages to be sent
    """
    
    
    telegram_token = '5800902618:AAEiZQ26G_4YUbS9eHafJohhZID3fsCEYLc'
    # Set the chat ID based on the channel name
    if channel == 'bollywood' or channel == 'hollywood':
        
        # Set the URL for the Telegram API's sendPhoto method using the TELEGRAM_TOKEN environment variable
        api_url   = f'https://api.telegram.org/bot{telegram_token}/sendPhoto'

        # Check if there are any rows in the dataframe
        if len(dataframe) > 0:
            # Iterate over the rows of the dataframe
            for i in range(len(dataframe)):
                # Use the shorten_url function to shorten the URL for the current row
                short_url = shorten_url(dataframe['link'][i])

                # Construct the description string using the values of the 'title', 'full_name', and 'link' columns for the current row
                description = f"\n{dataframe['title'][i]} \n\n{dataframe['full_name'][i]}" \
                              f"\n\nLink to Download:\n{short_url}"

                # Get the value of the 'image_link' column for the current row
                image_link = dataframe['image_link'][i]

               
                # Send a request to the Telegram API's sendPhoto method with the chat ID, description, and image link as arguments
                requests.post(api_url, json={'chat_id': chat_id, 'caption': description, 'photo': image_link})
                
            # print the message saying total message sposted in channel
            print(f"{len(dataframe)} Messages posted successfully in {channel} telegram channel.")
                
        else:
            # Return a message if there are no rows in the dataframe
            print("Not found any new post on website.")
            return False
               
    else:
        # Return an error message if the channel name is invalid
        print("Invalid channel type mentioned. Channel type can be either 'bollywood' or 'hollywood'.")
        return False



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
    bollywood_chat_id = '@moviesnut_bollywood'
    hollywood_chat_id = '@moviesnut_hollywood'
    
    send_to_telegram(channel = 'bollywood', dataframe = dotmovies_df, chat_id = bollywood_chat_id)
    send_to_telegram(channel = 'hollywood', dataframe = vegamovies_df, chat_id = hollywood_chat_id)


