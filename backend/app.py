from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/players', methods=['GET'])
def get_players():
    url = 'https://api.myfantasyleague.com/2024/export?TYPE=players&L=62247&DETAILS=1&JSON=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        players = data.get('players', {}).get('player', [])
        return jsonify(players)
    else:
        return jsonify({'error': 'Failed to fetch data from MFL'}, response.status_code)
    
if __name__ == '__main__':
    app.run(debug=True)