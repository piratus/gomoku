import React from 'react';
import cx from 'classnames';

import {login, setName} from '../actions/actions';
import UserStore from '../stores/UserStore';
import Modal from './Modal';


class ConnectionModal extends React.Component {

  static propTypes = {
    connected: React.PropTypes.bool.isRequired,
    self: React.PropTypes.object.isRequired
  };

  handleSubmit(event) {
    event.preventDefault();
    login(UserStore.getState().name);
  }

  render() {
    const {self, connected} = this.props;
    return (
      <Modal>
        {connected && <form onSubmit={this.handleSubmit}>
          <label htmlFor="username-input">
            What is your name?
          </label>
          <input id="username-input"
                 type="text"
                 className={cx({invalid: self.error})}
                 autoFocus={true}
                 value={self.name}
                 readOnly={self.isAuthenticated || self.locked}
                 onChange={({target})=> { setName(target.value); }} />
          {self.error && <span className="error-text">{self.error}</span>}
          {!self.isAuthenticated &&
            <button type="submit"
                    disabled={!self.name || self.locked || self.error}>
              Start playing
            </button>
          }
        </form>}
        {!connected &&
          <button type="submit" value="connect">
            Reconnect
          </button>
        }
      </Modal>
    );
  }

}


export default ConnectionModal;
