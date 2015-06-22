import createStore from 'flux-stateful';

import {dispatcher, client} from '../dispatcher';
import {Actions} from '../constants';


export default createStore(dispatcher, {
  getInitialState() {
    return {
      connected: client.isConnected,
      users: null,
      games: null
    };
  },

  [Actions.CLIENT_CONNECTION_OPEN]() {
    this.setState({connected: true});
  },

  [Actions.CLIENT_CONNECTION_CLOSED]() {
    this.setState({connected: false, users: null, games: null});
  },

  [Actions.CLIENT_BROADCAST]({users, games}) {
    this.setState({users, games});
  }
});
