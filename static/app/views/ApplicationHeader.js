import React from 'react';
import cx from 'classnames';

import '../../styles/_top-bar.scss';
import {leaveGame} from '../actions/actions';

export default class ApplicationHeader extends React.Component {

  static propTypes = {
    connected: React.PropTypes.bool.isRequired,
    self: React.PropTypes.object.isRequired,
    game: React.PropTypes.object.isRequired,
  };

  handleLeaveGame = (event)=> {
    event.preventDefault();
    leaveGame();
  };

  handleRankings = (event)=> {
    event.preventDefault();
    leaveGame();
  };

  render() {
    const {self, connected, game} = this.props;
    return (
      <header className="top-bar">
        <nav>
          <li>
            <i className={cx('socket-status', {'is-connected': connected})} />
          </li>
          {self.isAuthenticated &&
            <li><strong>{self.name}</strong></li>
          }
        </nav>
        <nav>
          {game.inProgress &&
            <li><a href="#" onClick={this.handleLeaveGame}>Leave game</a></li>
          }
        </nav>
      </header>
    );
  }

}
