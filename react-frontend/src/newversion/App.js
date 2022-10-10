// import logo from './logo.svg';
import Axios from 'axios';
import {useState} from 'react';
import './App.css';
import BlockItem from './BlockItem';
import TxItem from './TxItem';

function App() {
  const [miningState, setMiningState] = useState('');
  const [privateK, setPrivate] = useState('N/A');
  const [publicK, setPublic] = useState('N/A');
  const [balance, setBalance] = useState('N/A');
  const [blocks, setBlocks] = useState([{"index": 0, "previousHash": "", "timestamp": 1465154705, "data": ['a'], "hash": "91a73664bc84c0baa1fc75ea6e4aa6d1d20c5df664c724e3159aefc2e1186627", "difficulty": 0, "nonce": 0}]);
  const [peers, setPeers] = useState('');

  let flaskHost = "http://" + window.token;

  const getKeyPair = () => {
    Axios.get('http://localhost:5000/keypair').then((response) => {
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
    const publicKey = localStorage.getItem('publicKey');
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
    Axios.post(flaskHost + '/transaction', { "receiver": receiver, "amount": amount }).then((response) => {
      console.log("response: " + response.data);
    });
    // get public key from local storage
    // const amount = document.getElementById("amount").value;
    // const recipient = document.getElementById("recipient").value; 
    // const publicKey = localStorage.getItem('publicKey');
    // const privateKey = localStorage.getItem('privateKey');
    // Axios.post('http://localhost:5000/sendTransaction', {"publicKey": publicKey, "privateKey": privateKey}).then((response) => {
    //   console.log("response: " + response.data);
    //   // setBalance("balance:" + response.data);
    //   setMiningState("response: " + response.data);
    // });
  };

  const addPeerNode = () => {
    const peerIP = document.getElementById("newPeer").value;
    Axios.post(flaskHost+'/peer', { "peerIP": peerIP }).then((response) => {
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
      <p>Flask saying my port = {window.token}</p>
      <p>{miningState}</p>
      <button onClick={startMining}>startMining</button>

      <hr />
      <h1> Peer </h1>
      <div className='PeerContainer'>
        <input type="text" id="newPeer" name="newPeer" />
        <button onClick={addPeerNode}>add Peer</button>
        <button onClick={getPeerNodes}>query Peer</button>
      </div>
      <ul>
        {!(Array.isArray(peers) || peers.length>0) ? 'N/A' : peers.map((item,i) =>(
          <li key={i}>{item}</li>
        ))}
      </ul>

      <hr />
      <h1> Wallet </h1>
      <div className='WalletContainer'>
        <div>
          <p>{privateK}</p>
          <p>{publicK}</p>
          <button onClick={getKeyPair}>Get KeyPair</button>
          <p>{balance}</p>
          <button onClick={getBalance}>RefreshBalance</button>
        </div>
      </div>

      <hr />
      <h1> Send tx </h1>
      <div className='SendTxContainer'>
        <label htmlFor='receiver'>Receiver</label>
        <input type="text" id="receiver" name="receiver" />

        <label htmlFor='amount'>Amount</label>
        <input type="text" id="amount" name="amount" />

        <button onClick={sendTransaction}>SendTransaction</button>
      </div>

      <hr />
      <h1> btcsan block history </h1>
      <button onClick={getBlocks}>refresh Blocks</button>
      {
        !(Array.isArray(blocks) || blocks.length>0) ? '' : 
        <div className="BlockTxContainer">
          <div className="Blocks">
            <h2>Latest Blocks</h2>
            <table>
              <tbody>
              {
                blocks.map((block,i) =>(
                  <BlockItem key={i} block={block} />
                ))
              }
              </tbody>
            </table>
          </div>
          <div className="Transactions">
            <h2>Latest Transactions</h2>
            <table>
              <tbody>
                {
                  blocks.map((block,i) =>(
                    block.data ? block.data.map((tx,j) =>(
                      <TxItem key={i-j} tx={tx} block={block}/>
                    )) : ''
                  ))
                } 
              </tbody>
            </table>
          </div>
        </div>
      }
    </div>
  );
}

export default App;
