import os
import re
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify
from twilio.rest import Client
from bs4 import BeautifulSoup
from twilio.twiml.messaging_response import MessagingResponse
from datetime import date


app = Flask(__name__)
APP_ROOT = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
# Find these values at https://twilio.com/user/account
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

@app.route("/", methods=['POST'])
def answer():
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == '.':
        resp.message(getStatus())

    return str(resp)

def getStatus():
    soup = BeautifulSoup(requests.get("http://airechile.mma.gob.cl/comunas/temuco").text,features="html.parser")
    today =  date.today().strftime("%d/%m/%Y")
    tag = soup.find("h3",class_="panel-title")
    details = soup.find_all("div",class_="item-inner")
    text = 'Para hoy '+today+' en Temuco hay: *'+ tag.contents[0][1:-1]+'*\n'
    cleanr = re.compile('<.*?>')
    for tag in details:
        text = text + re.sub(cleanr, '', str(tag.contents[1]))+'\n'
    return text


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)