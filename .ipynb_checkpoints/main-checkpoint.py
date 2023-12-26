from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from flask import Flask
from flask import request
from langchain.schema import HumanMessage
import requests

load_dotenv()

app = Flask(__name__)
llm = OpenAI()

def chat_ai(message):
    messages = [HumanMessage(content=message)]
    response = llm.invoke(messages)
    return response

def sendMessage(message, id):
    response = {
        "recipient": {"id": id},
        "message": {
            "text": message
        },
        "messaging_type": "RESPONSE",
        "access_token": "EAAE0ZBcoYZBaIBO2AmWcpNFyAyx8OX9A28tmp6otE7dRn3KSSHa0Syeb5ooaY2deMapedCoJiuXf66O9ZCW9pzjkxIqinjGQIBJKRjs50PFGjmRs0vCkzRnqds5uth1mnZBLMZBwZC5ZBT5eMCu1IeMGXek2HBEgasi5o1NZBwgCHWEIe5ZCg6ZBMAFXNHKMlKKxYyaZBZCCYCN4BjlW4pb5ZCAJLdiEZD"
    }
    print(message, id)
    print(response)
    result = requests.post("https://graph.facebook.com/v18.0/107426468924642/messages", json=response)
    print(result)

@app.route("/", methods=["POST", "GET"])
def index():
    if (request.method == "GET"):
        return request.args.get('hub.challenge')
    try:
        message = request.json["entry"][0]["messaging"][0]["message"]["text"]
        sender_id = request.json["entry"][0]["messaging"][0]["sender"]["id"]
        response = chat_ai(message)
        sendMessage(response, sender_id)
    except:
        print("An error occured")
    return "test"

@app.route("/webhook", methods=["POST"])
def webhook():
    return "Webhook Received"
    
@app.route("/webhooks", methods=["GET"])
def webhooks():
    return "Webhook"

@app.route("/messaging-webhook", methods=["GET"])
def messageHook():
    print(request.data)
    return request.args.get('hub.challenge')

app.run(host="0.0.0.0", port="3001")