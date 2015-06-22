import createStore from 'flux-stateful';

import {dispatcher} from '../dispatcher';
import {Actions, GameState} from '../constants';


const {IN_PROGRESS, FINISHED} = GameState;

export default createStore(dispatcher, {
  getInitialState() {
    return {
      inProgress: false,
      board: null,
      state: null,
      turn: null,
      winner: null,
      black: null,
      white: null,
    };
  },

  [Actions.USER_UPDATE_STATE]({user}) {
    const {
      state=null,
      board=null,
      turn=null,
      winner=null,
      black=null,
      white=null,
    } = user.game || {};
    const inProgress = [IN_PROGRESS, FINISHED].includes(state);
    this.setState({
      state,
      board,
      turn,
      winner,
      black,
      white,
      inProgress,
    });
  },

  [Actions.CLIENT_CONNECTION_CLOSED]() {
    this.setState({
      iProgress: false,
      state: null,
      white: null,
      black: null,
      winner: null,
    });
  }
});
