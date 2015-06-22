import {Actions, ClientMessages, ServerMessages} from '../constants';
import {dispatch, client} from '../dispatcher';
import {SOCKET_OPEN_EVENT, SOCKET_CLOSED_EVENT} from '../util/SocketClient';


export function connect() {
  client.connect();
}

client.on(SOCKET_OPEN_EVENT, ()=> {
  dispatch(Actions.CLIENT_CONNECTION_OPEN);
});

client.on(SOCKET_CLOSED_EVENT, ({code, reason, wasClean})=> {
  dispatch(Actions.CLIENT_CONNECTION_CLOSED, {code, reason, wasClean});
});

client.on(ServerMessages.BROADCAST, (data)=> {
  dispatch(Actions.CLIENT_BROADCAST, data);
});

client.on(ServerMessages.USER_UPDATE_STATE, ({user})=> {
  dispatch(Actions.USER_UPDATE_STATE, {user});
});

client.on(ServerMessages.GAME_ERROR, (error)=> {
  dispatch(Actions.CLIENT_GAME_ERROR, error);
});

export function setName(name) {
  dispatch(Actions.USER_SET_NAME, {name});
}


export function login(name) {
  dispatch(Actions.USER_LOGIN_START);
  client.send(ClientMessages.USER_LOGIN, {name});
}


client.on(ServerMessages.USER_LOGIN_ERROR, ({detail})=> {
  dispatch(Actions.USER_LOGIN_ERROR, {detail});
});


export function createGame(side) {
  client.send(ClientMessages.GAME_CREATE, {side});
}

export function joinGame(id, side) {
  client.send(ClientMessages.GAME_JOIN, {id, side});
}

export function makeMove(side, x, y) {
  client.send(ClientMessages.GAME_MOVE, {side, x, y});
}

export function leaveGame() {
  client.send(ClientMessages.GAME_LEAVE);
}
