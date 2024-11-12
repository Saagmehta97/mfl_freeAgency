import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Player from './components/Player';
import './App.css';

interface PlayerData {
  id: string;
  name: string;
  position: string;
  team: string;
}

const App: React.FC = () => {
  const [players, setPlayers] = useState<PlayerData[]>([]);

  useEffect(() => {
    axios.get('/api/players')
      .then(response => {
          setPlayers(response.data)
      })
      .catch(error => {
        console.error('Error fetching player data: ', error);
      })
  }, []);
  
  return (
    <div className="App">
      <h1>Free Agency Players</h1>
      <div className="player-list">
          {players.map(player => (
            <Player
              key={player.id}
              id={player.id}
              name={player.name}
              position={player.position}
              team={player.team}
              />
          ))}
      </div>
    </div>
  );
};

export default App;
