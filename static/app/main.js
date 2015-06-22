import '../styles/app.scss';
import 'babel/polyfill';

import React from 'react';

import Application from './views/Application';
import {connect, login} from './actions/actions';
import {client} from './dispatcher';


if (DEBUG) {
  client.on('connection:open', ()=> {
    const lastUsedName = localStorage.name;
    if (lastUsedName) { login(lastUsedName); }
  });

  client.on('connection:closed', ()=> {
    setTimeout(()=> { connect(); }, 2000);
  });
}


React.render(
  <Application />,
  document.body
);

connect();
