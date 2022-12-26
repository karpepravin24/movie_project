import requests
import os


def shorten_url(url):
    # Hardcoded API token
    shrinkme_token = os.environ['SHRINKME_TOEKN']

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


def send_to_telegram(channel, dataframe):
    channel = channel.upper()
    if channel == 'bollywood' or channel == 'hollywood':
        telegram_token = os.environ['TELEGRAM_TOKEN']
        chat_id   = os.environ[f'{channel}_CHAT_ID']
        api_url   = f'https://api.telegram.org/bot{telegram_token}/sendPhoto'

        if len(dataframe) > 0:
            for i in range(len(dataframe)):
                short_url = shorten_url(dataframe['link'][i])
                description = f"\n{dataframe['title'][i]} \n\n{dataframe['full_name'][i]}" \
                              f"\n\nLink to Download:\n{short_url}"
                image_link = dataframe['image_link'][i]

                try:
                    response = requests.post(api_url, json={'chat_id': chat_id, 'caption': description, 'photo': image_link})
                except Exception as e:
                    print(e)
             print(f"{len(dataframe)} MEssages posted successfully in {channel} telegram channel")       
             
        else:
            return "Not found any new post on website."


    else:
        return "Invalid channel type mentioned. Channel type can be either 'bollywood' or 'hollywood'."

