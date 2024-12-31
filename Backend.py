from flask import Flask, request, jsonify
import requests

username = "o_4apqv74qgt"
password = "Workdone@2070"

auth_res = requests.post("https://api-ssl.bitly.com/oauth/access_token",auth=(username,password))

app = Flask(__name__)

BITLY_ACCESS_TOKEN = auth_res.content.decode()

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    long_url = data.get('long_url')
    if not long_url:
        return jsonify({'error': 'Missing long_url'}), 400

    headers = {
        'Authorization': f'Bearer {BITLY_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {'long_url': long_url}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', json=payload, headers=headers)

    if response.status_code == 200:
        short_url = response.json().get('link')
        return jsonify({'short_url': short_url})
    else:
        return jsonify({'error': 'Failed to shorten URL'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
