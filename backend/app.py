from flask import Flask, jsonify
import requests
from flask_caching import Cache
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if accessing the API from a different domain
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Replace with your actual league ID and franchise ID
LEAGUE_ID = '62247'
FRANCHISE_ID = '0008'  # Your franchise ID

@cache.cached(timeout=86400)
def fetch_player_details(status='ALL'):
    url = f'https://api.myfantasyleague.com/2024/export?TYPE=players&DETAILS=&SINCE=&STATUS={status}&JSON=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        players = data.get('players', {}).get('player', [])
        player_dict = {player['id']: player for player in players}
        return player_dict
    else:
        return {}

@cache.cached(timeout=3600)
def fetch_player_scores():
    url = f'https://api.myfantasyleague.com/2024/export?TYPE=playerScores&L={LEAGUE_ID}&W=YTD&JSON=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        player_scores = data.get('playerScores', {}).get('playerScore', [])
        scores_dict = {player['id']: float(player.get('score', 0)) for player in player_scores}
        return scores_dict
    else:
        return {}

@cache.cached(timeout=3600)
@app.route('/api/roster', methods=['GET'])
def get_roster():
    url = f'https://api.myfantasyleague.com/2024/export?TYPE=rosters&L={LEAGUE_ID}&FRANCHISE={FRANCHISE_ID}&JSON=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        player_ids = data.get('rosters', {}).get('franchise', [{}])[0].get('player', [])
        player_dict = fetch_player_details(status='ALL')
        roster_players = [player_dict.get(player['id']) for player in player_ids if player_dict.get(player['id'])]
        return jsonify(roster_players)
    else:
        return jsonify({'error': 'Failed to fetch roster from MFL'}), response.status_code

@cache.cached(timeout=3600)
@app.route('/api/free_agents', methods=['GET'])
def get_free_agents():
    url = f'https://api.myfantasyleague.com/2024/export?TYPE=freeAgents&L={LEAGUE_ID}&JSON=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        player_ids = data.get('freeAgents', {}).get('league', {}).get('player', [])
        player_dict = fetch_player_details(status='ACTIVE')
        free_agents = [player_dict.get(player['id']) for player in player_ids if player_dict.get(player['id'])]

        # Fetch player scores and add them to player data
        scores_dict = fetch_player_scores()
        for player in free_agents:
            player_id = player['id']
            player['score'] = scores_dict.get(player_id, 0)

        return jsonify(free_agents)
    else:
        return jsonify({'error': 'Failed to fetch free agents from MFL'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
