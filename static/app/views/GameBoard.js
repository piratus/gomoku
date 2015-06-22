import React from 'react';
import cx from 'classnames';

import {makeMove} from '../actions/actions';


/**
 * @class GameBoard
 * @extends React.Component
 */
export default class GameBoard extends React.Component {

  static propTypes = {
    board: React.PropTypes.arrayOf(
      React.PropTypes.arrayOf(React.PropTypes.number)),
    side: React.PropTypes.oneOf(['white', 'black']),
    winner: React.PropTypes.oneOf(['white', 'black']),
  };

  handleClick(x, y) {
    makeMove(this.props.side, x, y);
  }

  render() {
    return (
      <table className="game-board">
        <caption>
          {this.props.winner ?
            <h1>{this.props.winner.toUpperCase()} WINS!</h1> :
            <h1>{this.props.side}</h1>
          }
        </caption>
        {this.props.board.map((row, x)=>
          <tr className="game-board--row">
            {row.map((item, y)=>
              <td className="game-board--cell"
                  onClick={this.handleClick.bind(this, x, y)}>
                <span
                  className={cx({black: item === 1, white: item === 2})} />
              </td>
            )}
          </tr>
        )}
      </table>
    );
  }

}
