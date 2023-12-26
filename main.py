from flask import Flask, request, abort
from pprint import pprint
from dotenv import load_dotenv
import os
from chatbot import Chatbot
import requests

load_dotenv()
app = Flask(__name__)
token = os.environ['PAGE_ACCESS_TOKEN']
page_id = os.environ['PAGE_ID']

def sendMessage(id, message):
    try:
        response = {
            "recipient": {"id": id},
            "message": {
                "text": message
            },
            "messaging_type": "RESPONSE",
            "access_token": token
        }
        result = requests.post(f"https://graph.facebook.com/v18.0/{page_id}/messages", json=response)
    except Exception as e:
        print(e)
        print("An error occured")

@app.route('/webhook', methods=['GET'])
def webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if (mode and token):
        if (mode == "subscribe" and token == os.environ['VERIFY_TOKEN']):
            print("Webhook Verified")
            return challenge
    
    return abort(403)

@app.route('/webhook', methods=['POST'])
def handleWebhook():
    body = request.json

    if body['object'] == 'page':
        for entry in body['entry']:
            for webhookEvent in entry['messaging']:
                senderPsid = webhookEvent['sender']['id']
                message = webhookEvent['message']['text']
                chatbot = Chatbot(senderPsid)
                response = chatbot.chatAi(message)
                sendMessage(senderPsid, response.content)

    return "Hi"
