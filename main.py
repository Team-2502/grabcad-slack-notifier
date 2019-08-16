from flask import Flask, request
import os

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_grabcad_email():
    print(request.data)
    return '', 204

if __name__ == '__main__':
    debug = 'PRODUCTION' in os.environ.values()
    try:
        port = int(os.environ['PORT'])
    except KeyError:
        port = 5000


    app.run(debug=debug, port=port)
