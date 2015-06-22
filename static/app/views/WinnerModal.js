import React from 'react';

import Modal from './Modal';
import {leaveGame} from '../actions/actions';


/**
 * @class WinnerModal
 * @extends React.Component
 */
export default class WinnerModal extends React.Component {

  static propTypes = {
    self: React.PropTypes.object,
    game: React.PropTypes.object,
  };

  handleButton = (event)=> {
    event.preventDefault();
    leaveGame();
  };

  render() {
    const {game, self} = this.props;
    const isWinner = game.winner === self.side;

    const title = isWinner ? 'Congratulations!' : 'Bummer';
    const subtitle = isWinner ? 'You are a winner' : 'Better luck next time';

    return (

      <Modal className={isWinner ? 'modal-winner' : 'modal-bummer'}>
        <h2>{title}</h2>
        <h3>{subtitle}</h3>
        <form onSubmit={this.handleButton}>
          <button >Play one more</button>
        </form>
      </Modal>
    );
  }

}
