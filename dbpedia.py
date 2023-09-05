def annotate_text_with_dbpedia_api():
    """
    Annotate a given text. The request returns a JSON response with annotated details.
    Probably, the length limit of the text is 1000 words.

    The documentation of the API: https://www.dbpedia-spotlight.org/api

    """
    import requests

    # Define the DBpedia API base URL
    api_url = 'https://api.dbpedia-spotlight.org/en/'

    # Define the endpoint for annotation
    endpoint = 'annotate'

    # Define your example text
    example_text = "Barack Obama was born in Honolulu, Hawaii."

    # Define the headers to accept JSON
    headers = {'accept': 'application/json'}

    # Make a GET request to the annotation endpoint with the text as a query parameter and JSON headers
    response = requests.get(f'{api_url}{endpoint}', params={'text': example_text}, headers=headers)

    # Check the HTTP status code
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            annotations = response.json()

            # Process the annotations as needed
            for annotation in annotations['Resources']:
                print(f"Entity: {annotation['@surfaceForm']}\n\t{annotation['@types']}\n\tDBpedia URI: {annotation['@URI']}\n")
        except ValueError as e:
            print(f"Error decoding JSON response: {e}")
    else:
        print(f"Request failed with status code: {response.status_code}")


annotate_text_with_dbpedia_api()
