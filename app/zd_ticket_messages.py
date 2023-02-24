import zendesk_client


def load_zendesk_tickets(config):

    ticket_list = zendesk_client.search_zendesk_tickets(config)

    id_list = _process_id_list(ticket_list)
    description_list = _process_descriptions(config, id_list)
    
    # TODO move this part into a different file
    # Saving the ticket's descriptions as ticket_messages.txt
    with open('ticket_messages.txt', 'w') as f:
        f.write(str(description_list))


# Process a list of tickets to extract the IDs
def _process_id_list(ticket_list):
    id_list = []

    if ticket_list["results"]:
        for ticket in range(0, len(ticket_list["results"])):
            id_list.append(ticket_list["results"][ticket]["id"])
    return id_list

## Process the descriptions of the ticket chats
def _process_descriptions(config, id_list):
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
