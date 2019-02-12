import json
import os
import sys

import requests


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


def send_message(recipient_id, message_text):
    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)


def send_typing_on(recipient_id):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": 'typing_on'
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)


def send_typing_off(recipient_id):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "sender_action": 'typing_off'
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)


def send_quick_reply(recipient_id, message, arr_quick_reply_response):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message,
            "quick_replies": arr_quick_reply_response
        }

    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)


def send_location_reply(recipient_id, message):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message,
            "quick_replies": [
                {
                    "content_type": "location",
                    "title": "Location",
                    "payload": "LOCATION_PAYLOAD"
                }, {
                    "content_type": "text",
                    "title": "Nope",
                    "payload": "LOCATION_NEGATIVE_PAYLOAD"
                }
            ]
        }

    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    # if r.status_code != 200:
    #     log(r.status_code)
    #     log(r.text)


def send_list_templates(recipient, listitems):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    element_items = []
    for item in listitems:
        item_dict = {
            "title": item["name"],
            "subtitle": item["description"],
            "item_url": "https://m.me",
            "image_url": item["banner"],
            "buttons": [{
                "type": "web_url",
                "url": item["logo"],
                "title": "Go To Website"
            }, {
                "type": "web_url",
                "title": "Lets Go! 🚗",
                "url": "https://maps.google.com.sg/maps/dir//" + str(item["latitude"]) + "," + str(
                    item["longitude"]) + "/?hl=en"
            }, {
                "type": "postback",
                "title": "Not this one",
                "payload": "NOT_THIS_ONE",
            }],
        }
        element_items.append(item_dict)

    data = json.dumps({
        "recipient": {
            "id": recipient
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": element_items
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        # log(r.text)
