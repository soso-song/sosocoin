// import logo from './logo.svg';
import Axios from 'axios';
import {useState} from 'react';
import './App.css';

function App() {
  const [miningState, setMiningState] = useState('');
  const [privateK, setPrivate] = useState('');
  const [publicK, setPublic] = useState('');
  const [balance, setBalance] = useState('');
  const [blocks, setBlocks] = useState('');
  const [peers, setPeers] = useState('');

  let flaskHost = "http://"+window.token;

  const getPrivateKey = () => {
    Axios.get(flaskHost+'/keypair').then((response) => {
      // store private key in local storage
      localStorage.setItem('privateKey', response.data['privateKey']);
      localStorage.setItem('publicKey', response.data['publicKey']);
      // console.log("received:" + response.data);
      setPrivate(response.data['privateKey']);
      setPublic(response.data['publicKey']);
    });
  };

  // const getPublicKey = () => {
  //   // get private key from local storage
  //   const privateKey = localStorage.getItem('privateKey');
  //   Axios.post('http://localhost:5000/getPublicKey', {"privateKey": privateKey}).then((response) => {
  //     // store public key in local storage
  //     localStorage.setItem('publicKey', response.data);
  //     // console.log("received:" + response.data);
  //     setPrivate("publicKey:" + response.data);
  //   });
  // };
  const getBalance = () => {
    // get public key from local storage
    const publicKey = localStorage.getItem('publicKey');
    Axios.post(flaskHost+'/getBalance', {"publicKey": publicKey}).then((response) => {
      // console.log("received:" + response.data);
      setBalance("balance:" + response.data);
    });
  };

  const startMining = () => {
    // get public key from local storage
    // const publicKey = localStorage.getItem('publicKey');
    setMiningState("mining...");
    Axios.get(flaskHost+'/startMining').then((response) => {
      console.log("response: " + response.data);
      // setBalance("balance:" + response.data);
      setMiningState("response: " + response.data);
    });
  };

  const getBlocks = () => {
    Axios.get(flaskHost+'/blocks').then((response) => {
      let result = ""
      for (let i = 0; i < response.data.length; i++) {
        result += JSON.stringify(response.data[i]);
      }
      setBlocks(result);
    });
  };

  const sendTransaction = () => {
    const receiver = document.getElementById("receiver").value;
    const amount = document.getElementById("amount").value;
    Axios.post(flaskHost+'/transaction', {"receiver": receiver, "amount": amount}).then((response) => {
      console.log("response: " + response.data);
    });
  };

  const addPeerNode = () => {
    const peerIP = document.getElementById("newPeer").value;
    Axios.post(flaskHost+'/peer', { "peerIP": peerIP, "addBack": true }).then((response) => {
      console.log("response: " + response.data);
      // setBalance("balance:" + response.data);
      // setMiningState("response: " + response.data);
    });
  };

  const getPeerNodes = () => {
    Axios.get(flaskHost+'/peers').then((response) => {
      // let result = ""
      // for (let i = 0; i < response.data.length; i++) {
      //   result += JSON.stringify(response.data[i]);
      // }
      console.log("response: " + response.data);
      setPeers(response.data);
    });
  };

  return (
    <div className="App">
      <p>This frontend is connected with flask backend = {window.token}</p>
      <p>{miningState}</p>
      <button onClick={startMining}>startMining</button>

      <hr />
      <h1> Peer </h1>
      <input type="text" id="newPeer" name="newPeer" />
      <button onClick={addPeerNode}>add Peer</button>
      <button onClick={getPeerNodes}>query Peer</button>
      <p>{peers}</p>

      <hr />
      <h1> Wallet </h1>
      <button onClick={getPrivateKey}>GetPrivateKey</button>
      {/* <button onClick={getPublicKey}>GetPublicKey</button> */}
      {'\n'}
      <p>{privateK}</p>
      {'\n'}
      <p>{publicK}</p>
      {'\n'}
      <p>{balance}</p>
      <button onClick={getBalance}>refresh balance</button>
      {'\n'}

      <hr />
      <h1> Send tx </h1>
      <p>Receiver</p>
      <input type="text" id="receiver" name="receiver" />
      {'\n'}
      <p>Amount</p>
      <input type="number" id="amount" name="amount"/>
      {'\n'}
      <button onClick={sendTransaction}>SendTransaction</button>
      {'\n'}

      <hr />
      <h1> btcsan block history </h1>
      <button onClick={getBlocks}>refresh Blocks</button>
      <p>{blocks}</p>
    </div>
  );
}

export default App;
