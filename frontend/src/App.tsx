import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Player from './components/Player';
import './App.css';

interface PlayerData {
  id: string;
  name: string;
  position: string;
  team: string;
  score?: number;
}

const App: React.FC = () => {
  const [roster, setRoster] = useState<PlayerData[]>([]);
  const [groupedFreeAgents, setGroupedFreeAgents] = useState<{ [position: string]: PlayerData[] }>({});
  const [searchTerm, setSearchTerm] = useState('');
  const [collapsedPositions, setCollapsedPositions] = useState<{ [position: string]: boolean }>({});

  useEffect(() => {
    // Fetch roster
    axios.get('/api/roster')
      .then(response => {
        setRoster(response.data);
      })
      .catch(error => {
        console.error('Error fetching roster data: ', error);
      });

    // Fetch free agents and group them
    axios.get('/api/free_agents')
      .then(response => {
        const freeAgents: PlayerData[] = response.data;

        // Apply search filter
        const filteredFreeAgents = freeAgents.filter(player =>
          player.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          player.team.toLowerCase().includes(searchTerm.toLowerCase())
        );

        // Group free agents by position
        const groupedByPosition = filteredFreeAgents.reduce((groups, player) => {
          const position = player.position || 'Unknown';
          if (!groups[position]) {
            groups[position] = [];
          }
          groups[position].push(player);
          return groups;
        }, {} as { [position: string]: PlayerData[] });

        // Sort and limit players in each position group
        const TOP_N = 10;
        Object.keys(groupedByPosition).forEach(position => {
          groupedByPosition[position] = groupedByPosition[position]
            .sort((a, b) => (b.score || 0) - (a.score || 0))
            .slice(0, TOP_N);
        });

        setGroupedFreeAgents(groupedByPosition);
      })
      .catch(error => {
        console.error('Error fetching free agent data: ', error);
      });
  }, [searchTerm]);

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const toggleCollapse = (position: string) => {
    setCollapsedPositions(prevState => ({
      ...prevState,
      [position]: !prevState[position],
    }));
  };

  return (
    <div className="App">
      <h1>My Roster</h1>
      <div className="player-list">
        {roster.map(player => (
          <Player
            key={player.id}
            id={player.id}
            name={player.name}
            position={player.position}
            team={player.team}
          />
        ))}
      </div>

      <h1>Top Free Agents by Position</h1>
      <input
        type="text"
        placeholder="Search by name or team..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-bar"
      />
      <div className="free-agents">
        {Object.entries(groupedFreeAgents).map(([position, players]) => (
          <div key={position} className="position-group">
            <h2 onClick={() => toggleCollapse(position)} className="position-header">
              {position} {collapsedPositions[position] ? '+' : '-'}
            </h2>
            {!collapsedPositions[position] && (
              <div className="player-list">
                {players.map(player => (
                  <Player
                    key={player.id}
                    id={player.id}
                    name={player.name}
                    position={player.position}
                    team={player.team}
                    score={player.score}
                  />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
