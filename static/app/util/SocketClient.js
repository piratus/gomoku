import {EventEmitter} from 'events';


export const SOCKET_OPEN_EVENT = 'connection:open';
export const SOCKET_CLOSED_EVENT = 'connection:closed';


/**
 * Socket connection wrapper
 * @class SocketClient
 */
export default class SocketClient {

  /** @private */ _events = new EventEmitter();
  /** @private */ _socket = null;

  constructor(url) {
    this.url = url;
  }

  get isConnected() {
    return Boolean(this._socket) &&
      this._socket.readyState === WebSocket.OPEN;
  }

  /**
   * Start a connection
   */
  connect() {
    if (this.isConnected) {
      throw new Error('Attempted to connect while connected');
    }

    this._socket = new WebSocket(this.url);

    this._socket.onopen = ()=> {
      if (DEBUG) { console.log('SocketClient: connection open'); }
      this._events.emit(SOCKET_OPEN_EVENT);
    };

    this._socket.onclose = (event)=> {
      if (DEBUG) { console.log('SocketClient: connection closed', event.code, event); }
      this._events.emit(SOCKET_CLOSED_EVENT, event);
    };

    this._socket.onmessage = (event)=> {
      const {MESSAGE, BODY} = JSON.parse(event.data);
      if (DEBUG) { console.log(`SocketClient: message "${MESSAGE}" received`, event); }
      this._events.emit(MESSAGE, BODY);
    };
  }

  /**
   * Send a message to the server
   * @param {string} message
   * @param {object} payload
   */
  send(message, payload={}) {
    if (!this.isConnected) { throw new Error('socket is not connected'); }
    this._socket.send(JSON.stringify({MESSAGE: message, BODY: payload}));
  }

  /**
   * Register incoming message handler
   * @param {string} message
   * @param {Function} handler
   */
  on(message, handler) {
    this._events.on(message, handler);
  }

}
