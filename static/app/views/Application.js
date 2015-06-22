import React from 'react';

import UserStore from './../stores/UserStore';
import GameStore from './../stores/GameStore';
import WorldStore from './../stores/WorldStore';

import ConnectionModal from './ConnectionModal';
import WinnerModal from './WinnerModal';
import ApplicationHeader from './ApplicationHeader';
import Dashboard from './Dashboard';
import GameBoard from './GameBoard';


const STORES = [WorldStore, UserStore, GameStore];

export default class Application extends React.Component {

  componentDidMount() {
    this._unsubscribers = STORES.map((store)=>
        store.subscribe(()=> {
          this.forceUpdate();
        })
    );
  }

  componentWillUnmount() {
    this._unsubscribers.forEach((unsubscribe)=> {
      unsubscribe();
    });
  }

  render() {
    const world = WorldStore.getState();
    const self = UserStore.getState();
    const game = GameStore.getState();
    const connected = world.connected;

    return (
      <div id="application">
        <ApplicationHeader
          connected={connected}
          game={game}
          self={self} />
        <section>
          {game.inProgress ?
            <GameBoard {...game} side={self.side} name={self.name} />
            :
            <Dashboard {...world} self={self}/>
          }
        </section>
        {(!connected || !self.isAuthenticated) &&
          <ConnectionModal connected={connected} self={self} />
        }
        {game.winner &&
          <WinnerModal game={game} self={self} />
        }
      </div>
    );
  }

}
