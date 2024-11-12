from flask import Flask, jsonify
import requests
from flask_caching import Cache
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'}) #in-memory cache

@cache.cached(timeout=86400)
def fetch_player_details():
    url = 'https://api.myfantasyleague.com/2024/export?TYPE=players&DETAILS=&SINCE=&STATUS=ACTIVE&JSON=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        players = data.get('players', {}).get('player', [])
        player_dict = {player['id']: player for player in players}
        return player_dict
    else:
        return jsonify({'error': 'Failed to fetch data from MFL'}, response.status_code)
    
    
    
@cache.cached(timeout=3600)
@app.route('/api/roster', methods=['GET'])
def get_roster():
    franchise_id = '62247'
    url = f'https://api.myfantasyleague.com/2024/export?TYPE=rosters&L=62247&FRANCHISE={franchise_id}&JSON=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        player_ids = data.get('rosters', {}).get('franchise', [{}])[0].get('player', [])
        player_dict = fetch_player_details(STATUS='ALL')
        #Map player IDs to player details
        roster_players = [player_dict.get(player['id']) for player in player_ids if player_dict.get(player['id'])]
        return jsonify(roster_players)
    else:
        return jsonify({'error', 'Failed to fetch roster data'}), response.status_code
    
    
@cache.cached(timeout=3600)
@app.route('/api/free_agents', methods=['GET'])
def get_free_agents():
    url = 'https://api.myfantasyleague.com/2024/export?TYPE=freeAgents&L=62247&JSON=1'
    response = requests.get(url)
    if response.status.code == 200:
        data = response.json()
        player_ids = data.get('freeAgents', ()).get('league', {}).get('player', [])
        player_dict = fetch_player_details(STATUS='ACTIVE')
        # Map player ID's to player details
        free_agents = [player_dict.get(player['id']) for player in player_ids if player_dict.get(player['id'])]
        return jsonify(free_agents)
    else:
        return jsonify({'error', 'Failed to fetch free agents'}), response.status_code
    
def get_top_free_agents(position, limit=10):
    free_agents = get_free_agents()
    position_players = [player for player in free_agents if player['position'] == position]
    sorted_players = sorted(position_players, key=lambda x: x.get('projectedPoints', 0), reverse=True)
    return sorted_players[:limit]
    

if __name__ == '__main__':
    app.run(debug=True)