Dotcoin
-----

> In this assignment, you will build a small ledger-based blockchain similar to Bitcoin. The original Bitcoin [whitepaper](https://Bitcoin.org/Bitcoin.pdf) is an excellent resource however the tutorial [Naivecoin: a tutorial for building a cryptocurrency](https://lhartikk.github.io/) provides a simpler but yet comprehensive overview of the most important Bitcoin concepts.
>
> You are tasked to implement a Python version of Naivecoin called *Dotcoin*. The goal is not solely to translate this code into python but rather understand in details the Bitcoin mechanics. You code must work but your grade will also depend on your understanding of the concepts. You will likely be asked to explain your code during during a live meeting with the instructor. 

The blockchain will run within a [Docker container](https://thierrysans.me/CSCD27/doc/docker/) and use [Python Flask](https://palletsprojects.com/p/flask/) for the HTTP server (instead of Node Express in the tutorial) and the [Python Libsodium Library (PyNaCl)](https://pynacl.readthedocs.io/en/latest/) for the cryptography primitives.



#### Project Setup/Background

###### React as frontend + Flask as backend, all serve through Flask

your url+port is also repersenting the backend url+port since I chosed to compile the react frontend and serve it throught flask

- everything will still in docker container (requirement)
- each ip repersent one node

###### localhost:5000 frontend access localhost:5000 backend

you can using the application like a local node app, the private key is always stored in backend, React frontend could control Flask backend to run operations that using private key by sending some requests.

###### localhost:5000 frontend access localhost:5001 backend

by enter a new node address in React, we can accompulish using frontend with port 5000 send request to port 5001, and since they have different URL, some private requests like `post transaction` will blocked with less effort. the public requests like `get balance` will be approved, making user can use it as a wallet (query) application.



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

##### Test Flow 1

- Access http://localhost:5000/ click `query peer`
- Access http://localhost:5001/ click `query peer`
- Enter `http://localhost:5000/` to Peer section and click `query peer` in both node to check they are linked.

##### Test Flow 2

- Go back to http://localhost:5000/

- Click `get keypair` button, this will returns prot's public and private key.

  > Note: this operation can only be done when the frontend&backend with the same port, ie. since they are considered as one node, the private key will returned for texting purpose. But there is no function is depends on private key in frontend.

- Click `refresh balance` button this will display your balance

- Click `start mining` button twice, this will generate two blocks and `50*2` coins reward will send to public key you get above.

  > The mining difficulties is functioning with BLOCK_GENERATION_INTERVAL = DIFFICULTY_ADJUSTMENT_INTERVAL = 10(seconds, blocks), difficulites is starts with 0, you may  need click button multiple times to see it's changes 

- Click `refresh blocks` button to check there are 3 blocks, the first block is the built in genesis block

##### Test Flow 3

- Get http://localhost:5001/'s public key

- Go to http://localhost:5000/ and sent transaction with amount `90` to http://localhost:5001/ 

  > Note: this will require two txIn you created before and create two txOut by testing this way, you now can make some GET requests to see the detailed infomation:
  >
  > http://localhost:5000/unspentTxOuts  
  >
  > http://localhost:5000/transactionPool

- Click `start mining` to add the transaction to the block
- Click `refresh blocks` to see the transaction you make

##### Test Flow 4

- Click `sync with peers` (one direction sync) to replace your chain 

  - if peer's block is 1 block longer

  - if peer's block is multiple blocks longer




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

Since I choosed to compile the react frontend and serve it throught flask, there are a little bit effert required if you want to make change in frontend.

The source of frontend is located in `/react-frontend` once you finished change, run `npm run build` in the same directory, this will output two folders under flask's src folder: `/src/static` and `/src/templates`



Reference: [Naivecoin(javascript)](https://lhartikk.github.io/about/) by Lauri Hartikka

