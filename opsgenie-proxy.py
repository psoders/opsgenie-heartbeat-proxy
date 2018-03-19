#!/usr/bin/env python3

from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

if os.getenv('HEARTBEAT_URL') is None or os.getenv('OPSGENIE_API_KEY') is None:
    app.logger.critical('You have to set HEARTBEAT_URL and OPSGENIE_API_KEY as env!')
    exit(1)

app.config['HEARTBEAT_URL'] = os.getenv('HEARTBEAT_URL')
app.config['API_KEY'] = os.getenv('OPSGENIE_API_KEY')

app.logger.info( 'OpsGenieProxy started for Heartbeat %s', app.config['HEARTBEAT_URL'])


@app.route('/healthz', methods=['GET'])
def healthz():
    return 'OK!'


@app.route('/proxy', methods=['POST'])
def proxy():
    headers = {'Authorization': 'GenieKey '+app.config['API_KEY']}
    app.logger.debug('Sending GET request to OpsGenie API')
    r = requests.post(
        app.config['HEARTBEAT_URL'],
        headers=headers
    )
    try:
        j = r.json()
    except ValueError:
        j = {
            'message': 'Failed to decode OpsGenie response',
            'originalResponse': str(r.content),
        }
    return (jsonify(j), r.status_code)


def main():
    app.run(debug=bool(os.getenv('DEBUG', False)), host='0.0.0.0')


if __name__ == '__main__':
    main()
