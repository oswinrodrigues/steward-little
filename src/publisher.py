import csv
import json
import requests

from secret import SECRET_TOKEN, NOTION_DATABASE

def create_payload(entry):
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": NOTION_DATABASE
        },
        "properties": {
            "Description": {
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": { "content": entry["description"] }
                    }
                ]
            },
            "Date": {
                "type": "date",
                "date": { "start": entry["date"] }
            },
            "Amount": {
                "type": "number",
                "number": float(entry["amount"])
            },
            "Category": {
                "type": "select",
                "select": { "name": entry["category"] }
            },
            "Bank": {
                "type": "select",
                "select": { "name": entry["bank"] }
            }
        }
    }

    return payload

def send_payload_to_notion(payload):
    url = "https://api.notion.com/v1/pages"

    requests.post(url, headers = {
        "Authorization": "Bearer " + SECRET_TOKEN,
        "Notion-Version": "2022-02-22",
        "Content-Type": "application/json"
    }, data = json.dumps(payload))

def publish_transactions(f):
    with open(f, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            payload = create_payload(row)
            send_payload_to_notion(payload)
