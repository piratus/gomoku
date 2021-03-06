export const Actions = {
  CLIENT_BROADCAST: 'CLIENT_BROADCAST',
  CLIENT_CONNECTION_OPEN: 'CLIENT_CONNECTION_OPEN',
  CLIENT_CONNECTION_CLOSED: 'CLIENT_CONNECTION_CLOSED',
  CLIENT_GAME_ERROR: 'CLIENT_GAME_ERROR',

  USER_UPDATE_STATE: 'USER_UPDATE_STATE',
  USER_SET_NAME: 'USER_SET_NAME',
  USER_LOGIN_START: 'USER_LOGIN_START',
  USER_LOGIN_ERROR: 'USER_LOGIN_ERROR',
};

export const ClientMessages = {
  USER_LOGIN: 'USER_LOGIN',
  GAME_CREATE: 'GAME_CREATE',
  GAME_JOIN: 'GAME_JOIN',
  GAME_MOVE: 'GAME_MOVE',
  GAME_LEAVE: 'GAME_LEAVE',
};

export const ServerMessages = {
  BROADCAST: 'BROADCAST',
  USER_LOGIN_ERROR: 'USER_LOGIN_ERROR',
  USER_UPDATE_STATE: 'USER_UPDATE_STATE',
  GAME_ERROR: 'GAME_ERROR',
};

export const GameState = {
  EMPTY: 0,
  WAITING: 1,
  IN_PROGRESS: 2,
  FINISHED: 3,
};
