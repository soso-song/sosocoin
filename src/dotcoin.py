from tarfile import BLOCKSIZE
from flask import Flask, request, render_template
import requests
# from flask_socketio import SocketIO

from blockchain import *  # getBlockchain, generateNextBlock
# from wallet import generateKeypair#, getPublicKey
from p2p import handleBlockchainResponse

import init
init.init()

app = Flask(__name__)
app.debug = True


@app.route("/")
def my_index():
    return render_template('index.html',token=request.host)


@app.route('/keypair', methods=['GET'])
def getKeypairAPI():
    # privateKey, publicKey = generateKeypair()
    # result = {
    #     'privateKey': privateKey,
    #     'publicKey': publicKey
    # }
    # config.PUBLIC_KEY = publicKey
    # config.PRIVATE_KEY = privateKey
    result = {
        'privateKey': config.PRIVATE_KEY,
        'publicKey': config.PUBLIC_KEY
    }
    return result


# user can do this locally
@app.route('/getBalance', methods=['POST'])
def getBalanceAPI():
    publicKey = request.get_json()['publicKey']
    return str(getBalance(publicKey))
# # user can do this locally
# @app.route('/balance', methods=['GET'])
# def balanceAPI():
#     publicKey = request.get_json()['publicKey']
#     return str(getBalance(publicKey))


@app.route('/startMining', methods=['GET'])
def startMiningAPI():
    lastStatus = config.isMining
    config.isMining = True
    generateNextBlock()
    # return str(newBlock.__dict__)
    return 'Mining status: ' + str(lastStatus) + "->" + str(config.isMining)

# # doesn't make sense
# @app.route('/mineBlock', methods=['POST'])
# def mineBlockAPI():
#     newBlock = generateNextBlock()
#     return str(newBlock.__dict__)

@app.route('/blocks', methods=['GET'])
def getBlocksAPI():
    result = []
    for block in getBlockchain():
        blockDict = block.__dict__.copy()
        transactions = [tx.__dict__.copy() for tx in blockDict['data']]
        for transaction in transactions:
            transaction['txIns'] = [txIn.__dict__.copy() for txIn in transaction['txIns']]
            transaction['txOuts'] = [txOut.__dict__ .copy()for txOut in transaction['txOuts']]
        blockDict['data'] = transactions
        result.append(blockDict)
    return json.dumps(result)



@app.route('/unspentTxOuts', methods=['GET'])
def getUnspentTxOutsAPI():
    result = []
    for unspentTxOut in config.unspentTxOuts:
        result.append(unspentTxOut.__dict__.copy())
    return json.dumps(result)

@app.route('/transactionPool', methods=['GET'])
def getTransactionPoolAPI():
    # result = []
    transactions = [tx.__dict__.copy() for tx in config.transactionPool[:]]
    for transaction in transactions:
        transaction['txIns'] = [txIn.__dict__.copy() for txIn in transaction['txIns']]
        transaction['txOuts'] = [txOut.__dict__ .copy()for txOut in transaction['txOuts']]
    # result.append(transactions)
    return json.dumps(transactions)

@app.route('/transaction', methods=['POST'])
def sendTransactionAPI():
    # senderPk = request.get_json()['senderPk']
    receiver = request.get_json()['receiver']
    amount = int(request.get_json()['amount'])
    # signature = request.get_json()['signature']
    if amount < 0:
        return 'Invalid amount'
    transaction = sendTransaction(receiver, amount).__dict__.copy()
    transaction['txIns'] = [txIn.__dict__.copy() for txIn in transaction['txIns']]
    transaction['txOuts'] = [txOut.__dict__ .copy()for txOut in transaction['txOuts']]
    # print("broo----")
    # print(transaction)
    return json.dumps(transaction)



# @app.route('/encodedBlocks', methods=['GET'])
# def getEncodedBlocksAPI():
#     print("herere----------111------")
#     print(getBlockchain())
#     bytes_encoded = getBlockchain().encode('utf-8')
#     print(bytes_encoded)
#     return bytes_encoded

@app.route('/syncPeers', methods=['GET'])
def syncPeersAPI():
    result = []
    for peer in config.peers:
        peerPort = peer.replace('http://localhost:', '')
        result.append(syncLatestAPI(
            "http://host.docker.internal:"+peerPort))
    return result

# @app.route('/syncLatest', methods=['POST'])
def syncLatestAPI(peerIP):
    peerBlocksJson = requests.get(peerIP+'/blocks')
    peerBlocks = json.loads(peerBlocksJson.text)
    for i,peerBlock in enumerate(peerBlocks):
        for j, tx in enumerate(peerBlock['data']):
            tx['txIns'] = [TxIn(txIn['txOutId'], txIn['txOutIndex'], txIn['signature']) for txIn in tx['txIns']]
            tx['txOuts'] = [TxOut(txOut['address'], txOut['amount']) for txOut in tx['txOuts']]
            peerBlock['data'][j] = Transaction(tx['id'], tx['txIns'], tx['txOuts'])
        peerBlocks[i] = Block(peerBlock['index'], peerBlock['hash'], peerBlock['previousHash'], peerBlock['timestamp'], peerBlock['data'], peerBlock['difficulty'], peerBlock['nonce'])
    
    
    # print("herere--------222--------")
    # print(peerBlocks)

    # result = []
    # for block in peerBlocks:
    #     blockDict = block.__dict__.copy()
    #     transactions = [tx.__dict__.copy() for tx in blockDict['data']]
    #     for transaction in transactions:
    #         transaction['txIns'] = [txIn.__dict__.copy() for txIn in transaction['txIns']]
    #         transaction['txOuts'] = [txOut.__dict__ .copy()for txOut in transaction['txOuts']]
    #     blockDict['data'] = transactions
    #     result.append(blockDict)
    # return json.dumps(result)
    # print(response.content)

    # convert Response to Block
   
    # print(receivedBlocks)
    # requests.post(peerIP,json={'block': getLatestBlock().__dict__})
    # print("herere--------333--------")
    # print(getLatestBlock().__dict__['index'])
    # print(peerBlocks[0].__dict__['index'])
    return handleBlockchainResponse(peerBlocks) #peerBlocks#requests.get(peerIP+'/blocks').text#handleBlockchainResponse(response)

@app.route('/peers', methods=['GET'])
def getPeersAPI():
    return json.dumps(config.peers)

@app.route('/peer', methods=['POST'])
def addPeerAPI():
    peer = request.get_json()['peerIP']
    addBack = request.get_json()['addBack']
    # print("-----111")
    # print(peer)
    # print(addBack)
    # print(request.host.docker.internal)

    if not 'http://localhost:' in peer:
        return "only support http://localhost:**** for now, received: " + peer

    if peer[-1] == '/':
        peer = peer[:-1]

    if request.host in peer:
        return 'Cannot add self'

    if peer in config.peers:
        return request.host + ': already has peer ' + peer

    config.peers.append(peer)  
    result = request.host + ': added ' + peer

    if addBack:
        peerPort = peer.replace('http://localhost:', '')

        result += '\n'
        result += requests.post("http://host.docker.internal:"+peerPort+'/peer',
                json={'peerIP': "http://"+request.host, 'addBack': None}).text

        # if "http://host.docker.internal:" in result:
        #     result = result.replace("host.docker.internal:", "localhost:")
    return result #json.dumps(config.peers)

# for reference
# def signTxIn(transaction, txInIndex, privateKey, unspentTxOuts):
#     txIn = transaction.txIns[txInIndex]
#     txId = transaction.id
#     referencedUnspentTxOut = findUnspentTxOut(
#         txIn.txOutId, txIn.txOutIndex, unspentTxOuts)
#     if referencedUnspentTxOut == None:
#         print('could not find referenced txOut from unspentTxOuts')
#         # throw Error('could not find referenced txOut')
#         return None
#     referencedAddress = referencedUnspentTxOut.address
#     # check if the private key matches TxOut.address that has TxOut.amount coins from unspentTxOuts(history)
#     if getPublicKey(privateKey) != referencedAddress:
#         print('trying to sign an input with private' +
#               ' key that does not match the address that is referenced in txIn')
#         # throw Error()
#         return None
#     #key = ec.generate_private_key(int(privateKey, 16), ec.SECP256K1())
#     #signature = key.sign(dataToSign.encode('utf-8'), ec.ECDSA(hashes.SHA256()))
#     key = ecdsa.SigningKey.from_string(
#         bytes.fromhex(privateKey), curve=ecdsa.SECP256k1)
#     signature = key.sign(bytes.fromhex(txId))

#     return signature





# @app.route('/peers', methods=['GET'])
# def getPeersAPI():
#     #res.send(getSockets().map(( s: any ) => s._socket.remoteAddress + ':' + s._socket.remotePort));
#     return json.dumps(app.socket)

# @app.route('/addPeer', methods=['POST'])
# def addPeerAPI():
#     connectToPeers(request.body.peer)
#     return json.dumps()

# @app.route('/sendTransaction', methods=['POST'])
# def mineTransactionAPI():
#     address = request.form['address']
#     amount = request.form['amount']
#     resp = generatenextBlockWithTransaction(address, amount)
#     return json.dumps(resp)

# @app.route('/mineTransaction', methods=['POST'])
# def mineTransaction():
#     address = request.form['address']
#     amount = request.form['amount']
#     resp = generatenextBlockWithTransaction(address, amount)
#     return json.dumps(resp)

# app.run(debug=True, port=3001)