import createStore from 'flux-stateful';

import {dispatcher} from '../dispatcher';
import {Actions} from '../constants';


export default createStore(dispatcher, {
  getInitialState() {
    return {
      id: null,
      name: sessionStorage.name || '',
      game: null,
      isAuthenticated: false,
      locked: false,
      error: null,
    };
  },

  [Actions.USER_SET_NAME]({name}) {
    const {isAuthenticated, locked} = this.state;
    if (!isAuthenticated && !locked) {
      this.setState({name, error: null});
    }
  },

  [Actions.USER_UPDATE_STATE]({user}) {
    if (!this.state.name) {
      localStorage.name = user.name;
    }

    this.setState({
      ...user,
      locked: false,
    });

    sessionStorage.name = user.name;
  },

  [Actions.USER_LOGIN_START]() {
    this.setState({locked: true});
  },

  [Actions.USER_LOGIN_ERROR]({detail}) {
    this.setState({error: detail, locked: false});
  }
});
