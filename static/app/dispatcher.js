import {Dispatcher} from 'flux';

import SocketClient from './util/SocketClient';


/**
 * Main application dispatcher
 * @global
 */
export const dispatcher = new Dispatcher();

/**
 * Application's socket client
 * @global
 */
export const client = new SocketClient(`ws://${location.host}/socket`);

/**
 * Shortcut for dispatching an action
 * @param {string} actionType
 * @param {object} payload
 * @global
 */
export function dispatch(actionType, payload={}) {
  dispatcher.dispatch({actionType, ...payload});
}
