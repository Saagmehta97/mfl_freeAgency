import React from 'react'

interface PlayerProps {
    id: string;
    name: string;
    position: string;
    team: string;
}

const Player: React.FC<PlayerProps> = ({ id, name, position, team }) => {
    return (
        <div className="player-card">
            <h3>{name}</h3>
            <p>Position: {position}</p>
            <p>Team: {team}</p>
        </div>
    );
};

export default Player