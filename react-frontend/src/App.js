import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {useState,useEffect} from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Link from '@mui/material/Link';
import Balance from './Balance';
import Peer from './Peer';
import Blocks from './Blocks';
import SendTx from './SendTx';
import Mining from './Mining';
import PairKeys from './PairKeys';
// import Transactions from './Transactions';
import Axios from 'axios';

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Soso Song
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const mdTheme = createTheme();

let getBalance_post = 0
let keypair_get = null
let peers_get = []
let transaction_post = []
let blocks_get = []

function App() {
  const [miningState, setMiningState] = useState('');
  const [privateK, setPrivate] = useState('');
  const [publicK, setPublic] = useState('');
  const [blocks, setBlocks] = useState([]);
  const [balance, setBalance] = useState('');
  const [peers, setPeers] = useState([]);
  const [txs, setTxs] = useState([]);
  const [message,setMes] = useState('');
  // const getBalance = () => {
  //   setBalance(getBalance_post);
  // };
  // const sendTransaction = (receiver,amount) => {
  //   console.log(receiver);
  // };
  // const addPeerNode = (newPeer) => {
  //   console.log(newPeer);
  // };

  // const getPeerNodes = () => {
  //   setPeers(peers_get);
  // };

  // const getPairKeys = () => {
  //   setPrivate(keypair_get.privateKey);
  //   setPublic(keypair_get.publicKey);
  // }

  // const startMining = () => {
  //   console.log("start mining");
  // };

  // const getBlocks = () => {
  //   setBlocks(blocks_get);
  // };

  // const getTxs = () => {
  //   setTxs(transaction_post);
  // };
  // useEffect(() => {
  // getPairKeys()
  // getBalance()
  // getBlocks()
  // getPeerNodes()
  // });

  let flaskHost = "http://" + window.token;

  const getPairKeys = () => {
    Axios.get(flaskHost + '/keypair').then((response) => {
      // store private key in local storage
      localStorage.setItem('privateKey', response.data['privateKey']);
      localStorage.setItem('publicKey', response.data['publicKey']);
      // console.log("received:" + response.data);
      setPrivate(response.data['privateKey']);
      setPublic(response.data['publicKey']);
    });
  };

  const getBalance = () => {
    // get public key from local storage
    const publicKey = localStorage.getItem('publicKey');
    Axios.post(flaskHost + '/getBalance', { "publicKey": publicKey }).then((response) => {
      // console.log("received:" + response.data);
      setBalance(response.data);
    });
  };

  const sendTransaction = (receiver, amount) => {
    // const receiver = document.getElementById("receiver").value;
    // const amount = document.getElementById("amount").value;
    Axios.post(flaskHost + '/transaction', { "receiver": receiver, "amount": amount }).then((response) => {
      console.log("response: " + response.data);
      setMes("response: " + response.data);
    });
  };

  const startMining = () => {
    // get public key from local storage
    // const publicKey = localStorage.getItem('publicKey');
    setMiningState("mining...");
    Axios.get(flaskHost + '/startMining').then((response) => {
      console.log("response: " + response.data);
      // setBalance("balance:" + response.data);
      setMiningState("response: " + response.data);
    });
  };

  const getBlocks = () => {
    Axios.get(flaskHost + '/blocks').then((response) => {
      // let result = ""
      // for (let i = 0; i < response.data.length; i++) {
      //   result += JSON.stringify(response.data[i]);
      // }
      setBlocks(response.data);
    });
  };

  

  const addPeerNode = (peerIP) => {
    // const peerIP = document.getElementById("newPeer").value;
    Axios.post(flaskHost + '/peer', { "peerIP": peerIP, "addBack": true }).then((response) => {
      console.log("response: " + response.data);
      // setMes("response: " + response.data);
      // setBalance("balance:" + response.data);
      // setMiningState("response: " + response.data);
    });
  };

  const getPeerNodes = () => {
    Axios.get(flaskHost + '/peers').then((response) => {
      // let result = ""
      // for (let i = 0; i < response.data.length; i++) {
      //   result += JSON.stringify(response.data[i]);
      // }
      // setPeers(peers_get);
      console.log("response: " + response.data);
      setMes("response: " + response.data);
      setPeers(response.data);
    });
  };

  const syncPeers = () => {
    Axios.get(flaskHost + '/syncPeers').then((response) => {
      setMes("response: " + response.data);
      console.log("response: " + response.data);
    });
  };
  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) => theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={12} lg={12}>
                <Card
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                  }}
                >
                  <Mining startMining={startMining} miningState={miningState} message={message}/>
                </Card>
              </Grid>
              {/* Peers */}
              <Grid item xs={12} md={8} lg={9}>
                <Card
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    maxHeight: 480,
                    minHeight: 205,
                  }}
                >
                  <Peer peers={peers} getPeerNodes={getPeerNodes} addPeerNode={addPeerNode}/>
                </Card>
              </Grid>
              {/* Balance */}
              <Grid item xs={12} md={4} lg={3}>
                <Card
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height:'100%',
                  }}
                >
                  <Balance balance={balance} getBalance={getBalance}/>
                </Card>
              </Grid>
              {/* Send Transaction */}
              <Grid item xs={12} md={6} lg={6}>
                <Card
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height:'100%',
                  }}
                >
                  <SendTx sendTransaction={sendTransaction}/>
                </Card>
              </Grid>
              <Grid item xs={12} md={6} lg={6}>
                <Card
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    minheight: 200,
                    height:'100%',
                  }}
                >
                  <PairKeys getPairKeys={getPairKeys} privateK={privateK} publicK={publicK} />
                </Card>
              </Grid>
              {/* Blocks */}
              <Grid item xs={12}>
                <Card sx={{ p: 2, display: 'flex', flexDirection: 'column',overflow:'auto' }}>
                  <Blocks blocks={blocks} getBlocks={getBlocks} syncPeers={syncPeers}/>
                </Card>
              </Grid>
              {/* <Grid item xs={12}>
                <Card sx={{ p: 2, display: 'flex', flexDirection: 'column',overflow:'auto' }}>
                  <Transactions txs={txs} getTxs={getTxs}/>
                </Card>
              </Grid> */}
            </Grid>
            <Copyright sx={{ pt: 4 }} />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;