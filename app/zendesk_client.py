
from urllib.parse import urlencode
import requests


#
# Obtain a list of  from a search
#
def search_zendesk_tickets(config):

    # User credentials
    user = config("ZENDESK_USER")
    api_key = config("ZENDESK_API_KEY")

    # Strings values for queries. 
    subdomain = '' # For example: acme.zendesk.com. Your company set it.
    type = 'ticket'
    status = '' # For example: >=solved (solved + closed)
    tags = '' # Optional. For example: __recurrent_user__
    ticket_created_from = '' # Optional. For example: >=2022-07-01
    ticket_created_to = '' # Optional. For example: <=2022-09-30
    group1 = '' # Optional. For example: "Users from Spain". Only you/your company knows your groups inside Zendesk.
    group2 = '' # Optional. For example: "Users from Mexico". Only you/your company knows your groups inside Zendesk.
    
    params = {

        # A) Query for specific solved & closed tickets within a time frame:
        'query': f'\
                type:{type} \
                status{status} \
                tags:{tags} \
                created{ticket_created_from} \
                created{ticket_created_to} \
                group:"{group1}"  \
                group:"{group2}"'

        # B) Query for all open tickets that were created today! (You can modify the "created" query to 1hours, 4hours, etc) and delete the others "created" queries.
        #'query': 'type:ticket status:open created>1hours' # You can add groups or not, it's up to you.
    }

    # Set the request parameters.
    url = f'https://{subdomain}/api/v2/search.json?' + urlencode(params)
    user = user + '/token'
    pwd = api_key

    # Do the HTTP get request with try/except.
    try:
        response = requests.get(url, auth=(user, pwd))
    except:
        print("Something in the URL call or in the request module is wrong. Please check them.")
        exit()

    # Check for HTTP codes other than 200.
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()

    # Decode the JSON response into a dictionary and use the data.
    return response.json()


#
# Get ticket information by ticket ID
#
def get_ticket(config, ticket_id):

    # User credentials
    user = config("ZENDESK_USER")
    api_key = config("ZENDESK_API_KEY")

    # Strings values for queries. 
    subdomain = '' # For example: acme.zendesk.com. Your company set it.

    # The endpoint for "web" tickets.
    url = f'https://{subdomain}/api/v2/tickets/' + str(ticket_id) + '.json/'
    
    # Do the HTTP get request.
    response_descriptions = requests.get(url, auth=(user, api_key))

    # Check for HTTP codes other than 200.
    if response_descriptions.status_code != 200:
        print('Status:', response_descriptions.status_code, 'Problem with the request. Exiting.')
        exit()

    # Decode the JSON response into a dictionary and use the data.
    return response_descriptions.json()

def get_ticket_chat_description(config, ticket_id):

    # User credentials
    user = config("ZENDESK_USER")
    api_key = config("ZENDESK_API_KEY")

    subdomain = '' # For example: acme.zendesk.com. Your company set it.
    # The endpoint for "chat" tickets.
    url = f'https://{subdomain}/api/v2/tickets/' + str(ticket_id) + '/audits/'
    
    # Do the HTTP get request.
    response_chat_descriptions = requests.get(url, auth=(user, api_key))

    # Check for HTTP codes other than 200.
    if response_chat_descriptions.status_code != 200:
        print('Status:', response_chat_descriptions.status_code, 'Problem with the request. Exiting.')
        exit()

    # Decode the JSON response into a dictionary and use the data.
    return response_chat_descriptions.json()