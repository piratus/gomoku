import createStore from 'flux-stateful';

import {dispatcher} from '../dispatcher';
import {Actions, GameState} from '../constants';


const {IN_PROGRESS, FINISHED} = GameState;

export default createStore(dispatcher, {
  getInitialState() {
    return [];
  },

  [Actions.GAME_ERROR](error) {
    this.setState(this.state.concat([{
      detail: error.detail,
      time: new Date()
    }]));
  },

  [Actions.CLIENT_CONNECTION_CLOSED]() {
    this.setState(this.state.concat([{
      detail: 'Socket connection closed',
      time: new Date()
    }]));
  }
});
