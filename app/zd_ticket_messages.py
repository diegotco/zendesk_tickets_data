import zendesk_client

# From a config with data to search tickets, generate the list of descriptions
def read_zendesk_tickets(config):

    ticket_list = zendesk_client.search_zendesk_tickets(config)

    id_list =_get_ids_from_tickets(ticket_list)
    description_list = _get_ticket_descriptions_from_id_list(config, id_list)
    return description_list

def _get_ids_from_tickets(ticket_list):
    id_list = []

    if ticket_list["results"]:
        for ticket in range(0, len(ticket_list["results"])):
            id_list.append(ticket_list["results"][ticket]["id"])
    return id_list

# Get a list of ticket of descriptions for a given ticket id list.
# Internally splits the content of the ticket by using token words and
# makes another call to the API to read the real content.
def _get_ticket_descriptions_from_id_list(config, id_list):
    description_list = []
    # Looking into the tickets ID for the user's request text. Also called "descriptions" in Zendesk.
    for ticket in id_list:
        
        data_descriptions = zendesk_client.get_ticket(config, ticket)

        via = (data_descriptions["ticket"]).get("via")
        if via["channel"] == "web":
            description = (data_descriptions["ticket"]).get("description")
            description_list.append(description)
        else:
            # PART B) If the description is from a "chat" ticket:
            chat_descriptions = zendesk_client.get_ticket_chat_description(config, ticket)

            try:
                history_chats = _chat_messages(chat_descriptions) # Trying to get the text on the ticket.
                is_chat_live = len(history_chats) > 0

                if is_chat_live: # Checking if this field has text on it.
                    description_chat = history_chats[1]["message"]
                    description_list.append(description_chat)
                else:
                    print("The message is empty, maybe a chat is still active. Ticket number:", ticket) # In active chats the "history" field is empty.
            except:
                # print("There was an error reading content in ticket number:", ticket)
                continue

    return description_list

# Process a list of chats to extract messages
def _chat_messages(chat_descriptions):
    return (chat_descriptions["audits"][0]["events"][0]["value"]).get("history") # Trying to get the text on the ticket.
