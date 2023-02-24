import os
from urllib.parse import urlencode
import requests


# Load the user and the API Key from the .env file.
with open(".env") as f:
    for line in f:
        key, value = line.strip().split("=")
        os.environ[key] = value

# Access the user.
user = os.getenv("USER")

# Access the API key.
api_key = os.getenv("API_KEY")

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
data = response.json()

id_list = []
description_list = []

if data["results"]:
    for ticket in range(0, len(data["results"])):
        id_list.append(data["results"][ticket]["id"])
# print(id_list)

# Looking into the tickets ID for the user's request text. Also called "descriptions" in Zendesk.
for ticket in id_list:
    
    # PART A) If the description is from a "web" ticket:

    # The endpoint for "web" tickets.
    url = f'https://{subdomain}/api/v2/tickets/' + str(ticket) + '.json/'
    
    # Do the HTTP get request.
    response_descriptions = requests.get(url, auth=(user, pwd))

    # Check for HTTP codes other than 200.
    if response_descriptions.status_code != 200:
        print('Status:', response_descriptions.status_code, 'Problem with the request. Exiting.')
        exit()

    # Decode the JSON response into a dictionary and use the data.
    data_descriptions = response_descriptions.json()

    via = (data_descriptions["ticket"]).get("via")
    if via["channel"] == "web":
        description = (data_descriptions["ticket"]).get("description")
        description_list.append(description)
    else:
        # PART B) If the description is from a "chat" ticket:

        # The endpoint for "chat" tickets.
        url = f'https://{subdomain}/api/v2/tickets/' + str(ticket) + '/audits/'
        
        # Do the HTTP get request.
        response_chat_descriptions = requests.get(url, auth=(user, pwd))

        # Check for HTTP codes other than 200.
        if response_chat_descriptions.status_code != 200:
            print('Status:', response_chat_descriptions.status_code, 'Problem with the request. Exiting.')
            exit()

        # Decode the JSON response into a dictionary and use the data.
        chat_descriptions = response_chat_descriptions.json()

        try:
            history_chats = (chat_descriptions["audits"][0]["events"][0]["value"]).get("history") # Trying to get the text on the ticket.
            if len(history_chats) > 0: # Checking if this field has text on it.
                description_chat = history_chats[1]["message"]
                description_list.append(description_chat)
            else:
                print("The message is empty, maybe a chat is still active. Ticket number:", ticket) # In active chats the "history" field is empty.
        except:
            # print("There was an error reading content in ticket number:", ticket)
            continue

# Saving the ticket's descriptions as ticket_messages.txt
with open('ticket_messages.txt', 'w') as f:
    f.write(str(description_list))

# Optional: Creating a dict using the tickets ID as keys and the descriptions (web and chat) as values.
# dict = {}
# for i in range(0, len(id_list)):
#     dict[id_list[i]] = description_list[i]
