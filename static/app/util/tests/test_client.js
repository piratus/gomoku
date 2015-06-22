/* eslint-env mocha */
/* global MockSocket MockServer */
import expect from 'expect.js';

import SocketClient from '../SocketClient';


window.WebSocket = MockSocket;

describe('SocketClient', ()=> {

  describe('connection', ()=> {
    const client = new SocketClient('ws://test-host/1');
    const server = new MockServer('ws://test-host/1');

    it('should emit an event on connect', (done)=> {
      expect(client.isConnected).to.eql(false);

      client.on('connection:open', ()=> {
        expect(client.isConnected).to.be(true);
        done();
      });

      client.connect();
    });

    it('should emit an event on disconnect', (done)=> {
      client.on('connection:closed', ()=> {
        expect(client.isConnected).to.be(false);
        done();
      });

      server.close();
    });
  });

  describe('message handling', ()=> {
    const client = new SocketClient('ws://test-host/2');
    const server = new MockServer('ws://test-host/2');

    before((done)=> {
      client.on('connection:open', ()=> { done(); });
      client.connect();
    });

    it('should parse incoming message', (done)=> {
      client.on('SERVER_MESSAGE', (payload)=> {
        expect(payload).to.eql({test: 'data'});
        done();
      });

      server.send(JSON.stringify({
        MESSAGE: 'SERVER_MESSAGE',
        BODY: {test: 'data'}
      }));
    });

    it('should send messages', (done)=> {
      server.on('message', (data)=> {
        expect(JSON.parse(data))
          .to.eql({MESSAGE: 'CLIENT_MESSAGE', BODY: {data: 'test'}});
        done();
      });

      client.send('CLIENT_MESSAGE', {data: 'test'});
    });
  });

});
