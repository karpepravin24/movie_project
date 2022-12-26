import json

def dump_latest_url(vegamovies_url, dotmovies_url, json_file_path):
    with open(json_file_path, 'w') as f:
        json.dump({'vegamovies_url': vegamovies_url, 'dotmovies_url': dotmovies_url}, f)

    print("URL saved successfully in JSON file:  'url_domain_names.json'")


def get_updated_url(json_file_path):
    """
    Read a JSON file and return the values of the 'vegamovies_url' and 'dotmovies_url' fields.

    Parameters:
        json_file_path (str): The file path to the JSON file.

    Returns:
        url_dict (dict): A dictionary containing the 'vegamovies_url' and 'dotmovies_url' fields.
    """

    # Open the JSON file and parse its contents
    with open(json_file_path) as f:
        url_dictionary = json.load(f)

    # Return the dictionary
    return url_dictionary


def get_last_run_results(domain):
    if domain == 'vegamovies' or domain == 'dotmovies':
        file_name = f"{domain}_last_run.json"
    else:
        return "Invalid Domain name given It can be either 'vegamovies' or 'dotmovies'"

    with open(file_name) as f:
        values = json.load(f)

    return values


def dump_latest_run_results(domain, dataframe):
    """
    Save the full names of movies from a Pandas dataframe to a JSON file.

    Parameters:
        domain (str): The name of the file to be saved. Can be either 'vegamovies' or 'dotmovies'.
        dataframe (pandas.DataFrame): A Pandas dataframe containing the movie data.

    Returns:
        str: An error message if the domain name is invalid. Otherwise, returns None.
    """

    # Set the file name based on the domain
    if domain == 'vegamovies' or domain == 'dotmovies':
        file_name = f"{domain}_last_run.json"
    else:
        return "Invalid Domain name given It can be either 'vegamovies' or 'dotmovies'"

    # Open the file in write mode and write the data to the file
    with open(file_name, 'w') as f:
        json.dump(dataframe['full_name'].tolist(), f)



