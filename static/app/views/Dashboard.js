import React from 'react';

import '../../styles/_dashboard.scss';

import {createGame, joinGame} from '../actions/actions.js';


export default class Dashboard extends React.Component {

  static propTypes = {
    self: React.PropTypes.object,
    games: React.PropTypes.array,
    users: React.PropTypes.array,
  };

  startAsBlack = ()=> createGame('black');
  startAsWhite = ()=> createGame('white');

  render() {
    const {self, games} = this.props;
    const grouped = (games || []).reduce((obj, game)=> {
      if (game.black && game.white) {
        obj.full.push(game);
      }
      else {
        obj.waiting.push(game);
      }
      return obj;
    }, {full: [], waiting: []});
    return (
      <div className="dashboard">

        {grouped.waiting.length > 0 &&
          <ul className="games-list">
            <li className="header"><h3>Waiting for players</h3></li>
            {grouped.waiting.map((game)=>
              <li className="game">
                {game.black ?
                  <span className="player player-black">{game.black.name}</span>
                  :
                  <button className="black"
                          onClick={()=> joinGame(game.id, 'black')}>
                    Join as black
                  </button>
                }
                <span className="separator">vs</span>
                {game.white ?
                  <span className="player player-white">{game.white.name}</span>
                  :
                  <button className="white"
                          onClick={()=> joinGame(game.id, 'white')}>
                    Join as white
                  </button>
                }
              </li>
            )}
          </ul>
        }
        {!self.game &&
          <ul className="games-list">
            <li className="header"><h3>Start new game</h3></li>
            <li className="game">
              <button className="black" onClick={this.startAsBlack}>
                Start as black
              </button>
              <span className="separator">vs</span>
              <button className="white" onClick={this.startAsWhite}>
                Start as white
              </button>
            </li>
          </ul>
        }

      </div>
    );
  }

}
