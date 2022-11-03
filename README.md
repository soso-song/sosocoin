Sosocoin
-----

#### Introduction

This project is a ledger-based blockchain for me to become familiar with the underlying logic of Bitcoin.  It covers the essential concepts, including proof of work, race conditions, validation, transactions (pool), and non-deterministic wallet.
I also wrote a React frontend that allows you to access each node's state on localhost when you run multiple instances (=node) with Docker for debugging and testing purposes.

> The original Bitcoin [whitepaper](https://Bitcoin.org/Bitcoin.pdf) is an excellent resource; however, the tutorial [Naivecoin: a tutorial for building a cryptocurrency](https://lhartikk.github.io/) (Typescript) provides a more straightforward yet comprehensive overview of the essential Bitcoin concepts.



#### Project Setup

##### Build the docker image (first time only)

```
docker build -t dotcoin .
```

To run your code in debug mode (the server will automatically reload when the source files change)

##### Add a node running on port 5000

```
docker run --rm -p 5000:5000 -v $(pwd)/src:/shared dotcoin flask --app dotcoin.py --debug run --host=0.0.0.0 -p 5000
```

Now you should able to access the first node by accessing localhost:5000

##### Add a node running on port 5001

```
docker run --rm -p 5001:5001 -v $(pwd)/src:/shared dotcoin flask --app dotcoin.py --debug run --host=0.0.0.0 -p 5001
```

> Type `ctrl-c` to stop the server. 



#### What is happening

Each node instance runs in a [Docker container](https://thierrysans.me/CSCD27/doc/docker/) and uses a [Python Flask HTTP server](https://palletsprojects.com/p/flask/) for user interaction.

![relation](/Users/sososong/Desktop/github_temp/sosocoin/media/relation.png)

##### React as frontend + Flask as backend, all serve through Flask

Serving React with a Flask backend means Flask will respond with a React webpage when the "/" page is requested.  The following code from `./src/dotcoin.py` handles the `http://localhost:5000/` `GET` request.

```python
app = Flask(__name__)
@app.route("/")
def my_index():
    return render_template('index.html',token=request.host)
```

##### Container networking

I'm avoiding using `--net=host` to simulate the "network" with each Docker container having its own network stack.

I define the **port of the Docker** instance and the **port in the Docker** that runs the Flask HTTP server sharing the same number (for each node).

A node running in a container consisted of a React frontend and a Flask backend; therefore, I let them have the same port number to make it easier to distinguish between them.

 - The frontend and Backend are inside a single Docker container, making the setup stable and simple.
 - Each number represents a unique node, no matter whether you are inside any container or not.

##### localhost:5000 frontend access localhost:5000 backend

> A node is accessing its own backend

Since the frontend and backend use the same port number, they represent the same node. All the requests will consider as the node's internal call. Therefore The Flask backend will handle any requests from the frontend, including getting the private key.

##### localhost:5000 frontend access localhost:5001 backend

> A miner/node interacts with another miner/node.

Frontend with port 5000 can send the request to the backend of the node hosting at port 5001, and since the sender is "node 5000" and the receiver is "node 5001", the requests will be handled as external calls. Therefore the requests that require the private key will not perform, including post `/transaction`, get `/keypair`. 

The requests like `/getBalance`, will be performed so that users can use it as a wallet (query) application.



#### Testing

##### Test Flow 1 (add peer node)

- Access http://localhost:5000/ click `peer->refresh button`

- Access http://localhost:5001/ click `peer->refresh button`

  > run  `npm run build` under `/react-frontend` if page is not working (check Contribution section)

- Enter `http://localhost:5000/` to the Peer section and click the "+" symbol.

- Click  `peer->refresh button` in both nodes to check they are linked.

##### Test Flow 2 (adding a block, mint coins, and mining function)

- Go back to http://localhost:5000/

- Click `keypair->refresh button` , this will returns the node's public and private keys.

  > Note: this operation can only be done when the request is considered as the node's [internal request](localhost:5000 frontend access localhost:5000 backend).

- Click `balance->refresh button`  this will display your balance = 0

- Click `blocks->refresh button` you should see the only block in the chain -  genesis block.

- Click the start mining button twice, which generates two blocks. The blockchain will send 50*2 coins as a reward to your public key.

  > The mining difficulty level is defined as 
  >
  > BLOCK_GENERATION_INTERVAL = DIFFICULTY_ADJUSTMENT_INTERVAL = 10(seconds, blocks)
  >
  > Difficulties start with 0. You may need to click the button multiple times to notice the delay.
  >
  > You can change the `STARTING_DIFFICULTY` in `/src/init.py` ( `21`~`23` takes 10 seconds on my 2017 Macbook pro)

- Click `blocks->refresh button` to check there are 3 blocks, and check your balance.

##### Test Flow 3 (send transaction)

- Copy http://localhost:5001/'s public key

- Go to http://localhost:5000/ and send a transaction with the amount of `90` to that public key

  > Note: this will require two [Unspent TX Outputs](https://en.wikipedia.org/wiki/Unspent_transaction_output) with the amount of 50 that mint/reward to you in Test Flow 2, then create two txOut. 
  >
  > You can now make some HTTP requests to see the detailed information:
  >
  > `GET` `http://localhost:5000/unspentTxOuts  `
  >
  > `GET` `http://localhost:5000/transactionPool`

- Click `start mining` to add the transaction to the block
- Click `blocks->refresh button` to see the transaction you made

##### Test Flow 4 (sync blocks)

> You can click the sync button in "node:5000", then check that nothing is happing, then click the button in "node:5001", then expect the number of blocks in "node:5001" should increase from 1 to 4.

- Click `sync with peers` (one-direction sync) to replace your chain 
  - if peer's block is 1 block longer

  - if peer's block is multiple blocks longer

- Click `blocks->refresh button` to compare two nodes before and after sync.




#### API Sandbox

##### GET Requests

```python
http://localhost:5000/startMining
http://localhost:5000/blocks
http://localhost:5000/unspentTxOuts
http://localhost:5000/transactionPool
http://localhost:5000/keypair	#A good example adds extra works to React -> require same url:port
http://localhost:5000/peers
http://localhost:5000/syncPeers
```

##### POST Requests

```python
http://localhost:5000/transaction
http://localhost:5000/getBalance
http://localhost:5000/peer
```



#### Contribution

Since I chose to compile the react frontend and serve it through flask, a little effort is required if you want to change the frontend.

The source of the frontend is located in `./react-frontend`, once you finished the change, run `npm run build` in the same directory, this will output two folders under Flask's src folder: `./src/static` and `/src/templates`

You might want to uncomment the following lines inside Dockerfile.

```
RUN npm install @mui/material @emotion/react @emotion/styled
RUN npm install @mui/icons-material
```



Reference: [Naivecoin(javascript)](https://lhartikk.github.io/about/) by Lauri Hartikka

