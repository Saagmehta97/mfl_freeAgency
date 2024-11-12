import React from 'react';

interface PlayerProps {
  id: string;
  name: string;
  position: string;
  team: string;
  score?: number;
}

const Player: React.FC<PlayerProps> = ({ id, name, position, team, score }) => {
  return (
    <div className="player-card">
      <h3>{name}</h3>
      <p>Position: {position}</p>
      <p>Team: {team}</p>
      {score !== undefined && <p>Score: {score.toFixed(2)}</p>}
    </div>
  );
};

export default Player;
