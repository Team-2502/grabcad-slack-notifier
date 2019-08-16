from flask import Flask, request
import os
import requests
from email_parser import parse_email

app = Flask(__name__)

KEY = os.environ['IFTTT_GRABCAD_KEY']
IFTTT_OUTBOUND_URL = f"https://maker.ifttt.com/trigger/grabcad_email_parsed/with/key/{KEY}"


@app.route('/', methods=['POST'])
def handle_grabcad_email():
    try:
        unescaped_email = request.data.decode('utf-8').encode('utf-8').decode('unicode_escape')
        slack_message = parse_email(unescaped_email)
        print(slack_message)
        requests.post(IFTTT_OUTBOUND_URL, json={'value1': slack_message})

        return '', 204
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    debug = 'PRODUCTION' in os.environ.values()
    try:
        port = int(os.environ['PORT'])
    except KeyError:
        port = 5000

    app.run(debug=debug, port=port)
