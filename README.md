Dotcoin
-----

> In this assignment, you will build a small ledger-based blockchain similar to Bitcoin. The original Bitcoin [whitepaper](https://Bitcoin.org/Bitcoin.pdf) is an excellent resource however the tutorial [Naivecoin: a tutorial for building a cryptocurrency](https://lhartikk.github.io/) provides a simpler but yet comprehensive overview of the most important Bitcoin concepts.
>
> You are tasked to implement a Python version of Naivecoin called *Dotcoin*. The goal is not solely to translate this code into python but rather understand in details the Bitcoin mechanics. You code must work but your grade will also depend on your understanding of the concepts. You will likely be asked to explain your code during during a live meeting with the instructor. 

The blockchain will run within a [Docker container](https://thierrysans.me/CSCD27/doc/docker/) and use [Python Flask](https://palletsprojects.com/p/flask/) for the HTTP server (instead of Node Express in the tutorial) and the [Python Libsodium Library (PyNaCl)](https://pynacl.readthedocs.io/en/latest/) for the cryptography primitives.



#### Project Setup/Background

###### React as frontend + Flask as backend, all serve through Flask

your url+port is also representing the backend url+port since I chose to compile the react frontend and serve it throught flask

- everything will still be in a docker container (requirement)
- each ip represents one node

###### localhost:5000 frontend access localhost:5000 backend

you can use the application like a local node app, the private key is always stored in the backend, React frontend could control Flask backend to run operations that use a private key by sending some requests.

###### localhost:5000 frontend access localhost:5001 backend

by entering a new node address in React, we can use the frontend with port 5000 to send request to port 5001, and since they have different URLs, some private requests like `post transaction` will blocked with less effort. Public requests like `get balance` will be approved, so that users can use it as a wallet (query) application.



#### Get Start

###### Build the docker image (first time only)

```
docker build -t dotcoin .
```

To run your code in debug mode (the server will automatically reload when the source files change)

###### Add node 1:

```
docker run --rm -p 5000:5000 -v $(pwd)/src:/shared dotcoin flask --app dotcoin.py --debug run --host=0.0.0.0 -p 5000
```

###### Add node 2:

```
docker run --rm -p 5001:5001 -v $(pwd)/src:/shared dotcoin flask --app dotcoin.py --debug run --host=0.0.0.0 -p 5001
```

> Type `ctrl-c` to stop the server. 

###### Testing:

##### Test Flow 1

- Access http://localhost:5000/ click `peer->refresh button`

- Access http://localhost:5001/ click `peer->refresh button`

  > run  `npm run build` under `/react-frontend` if page is not working (check Contribution section)

- Enter `http://localhost:5000/` to Peer section and click "+" symbol.

- Click  `peer->refresh button` in both nodes to check they are linked.

##### Test Flow 2

- Go back to http://localhost:5000/

- Click `keypair->refresh button` , this will returns port's public and private key.

  > Note: this operation can only be done when the frontend & backend with the same port, ie. since they are considered as one node, the private key will returned for testing purposes. But there are no functions that depend on private key in frontend.

- Click `balance->refresh button`  this will display your balance

- Click `start mining` button twice, this will generate two blocks and `50*2` coins as a reward will be sent to the public key you get above.

  > The mining difficulty level is represented with BLOCK_GENERATION_INTERVAL = DIFFICULTY_ADJUSTMENT_INTERVAL = 10(seconds, blocks), difficulites starts with 0, you may need to click the button multiple times to see its changes 

- You can change the `STARTING_DIFFICULTY` in `/src/init.py` ( `21`~`23` takes 10 seconds on my 2017 Macbook pro)

- Click `blocks->refresh button` button to check there are 3 blocks, the first block is the built in genesis block

##### Test Flow 3

- Get http://localhost:5001/'s public key

- Go to http://localhost:5000/ and sent transaction with amount `90` to http://localhost:5001/ 

  > Note: this will require two txIn you created before and create two txOut by testing this way, you now can make some GET requests to see the detailed infomation:
  >
  > http://localhost:5000/unspentTxOuts  
  >
  > http://localhost:5000/transactionPool

- Click `start mining` to add the transaction to the block
- Click `blocks->refresh button` to see the transaction you make

##### Test Flow 4

- Click `sync with peers` (one direction sync) to replace your chain 

  - if peer's block is 1 block longer

  - if peer's block is multiple blocks longer

- Click `blocks->refresh button` to see




#### API Sandbox

###### GET Requests

```python
http://localhost:5000/startMining
http://localhost:5000/blocks
http://localhost:5000/unspentTxOuts
http://localhost:5000/transactionPool
http://localhost:5000/keypair	#A good example adds extra works to React -> require same url:port
http://localhost:5000/peers
http://localhost:5000/syncPeers
```

###### POST Requests

```python
http://localhost:5000/transaction
http://localhost:5000/getBalance
http://localhost:5000/peer
```



#### Contribution

Since I chose to compile the react frontend and serve it throught flask, there is a little bit of effort required if you want to make change in frontend.

The source of the frontend is located in `/react-frontend` once you finished the change, run `npm run build` in the same directory, this will output two folders under flask's src folder: `/src/static` and `/src/templates`

You might want to include the following commands inside Dockerfile

```
RUN npm install @mui/material @emotion/react @emotion/styled
RUN npm install @mui/icons-material
```



Reference: [Naivecoin(javascript)](https://lhartikk.github.io/about/) by Lauri Hartikka

