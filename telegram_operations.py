import requests
import os


def shorten_url(url):
    # Hardcoded API token
    shrinkme_token = os.environ["SHRINKME_TOKEN"]

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



def send_to_telegram(channel, dataframe, chai_id, telegram_token):
    """Sends a message to a Telegram channel with a description and image for each row in a dataframe.

    Arguments:
    channel -- the name of the Telegram channel to send the message to (either 'vegamovies' or 'dotmovies')
    dataframe -- a Pandas dataframe with columns 'title', 'full_name', 'image_link', and 'link'
    """
    
    

    # Set the chat ID based on the channel name
    if channel == 'vegamovies' or channel == 'dotmovies':
        
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

                try:
                    # Send a request to the Telegram API's sendPhoto method with the chat ID, description, and image link as arguments
                    response = requests.post(api_url, json={'chat_id': chat_id, 'caption': description, 'photo': image_link})
                except Exception as e:
                    # Print any exceptions that are raised
                    print(e)
        else:
            # Return a message if there are no rows in the dataframe
            return "Not found any new post on website."
               
    else:
        # Return an error message if the channel name is invalid
        return "Invalid channel type mentioned. Channel type can be either 'bollywood' or 'hollywood'."

    


