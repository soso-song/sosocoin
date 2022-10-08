import hashlib
import time
import json

from transaction import getCoinbaseTransaction, isValidAddress, processTransactions, Transaction, UnspentTxOut, TxIn, TxOut
# , updateTransactionPool
from transactionPool import addToTransactionPool, getTransactionPool
from wallet import initWallet, createTransaction, findUnspentTxOuts, getBalance, getPrivateFromWallet, getPublicFromWallet


class Block:
    def __init__(self, index, hash, previousHash, timestamp, data, difficulty, nonce):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.difficulty = difficulty
        self.nonce = nonce

def calculateHashForBlock(block):
    return calculateHash(block.index, block.previousHash, block.timestamp, block.data, block.difficulty, block.nonce)

def calculateHash(index, previousHash, timestamp, data, difficulty, nonce):
    blockStr = str(index) + previousHash + str(timestamp) + str(data) + str(difficulty) + str(nonce)
    return hashlib.sha256(blockStr.encode('utf-8')).hexdigest()

def getCurrentTimestamp():
    return int(time.time())

def generateRawNextBlock(blockData):
    previousBlock = getLatestBlock()
    difficulty = getDifficulty(getBlockchain())
    nextIndex = previousBlock.index + 1
    nextTimestamp = getCurrentTimestamp()
    newBlock = findBlock(nextIndex, previousBlock.hash,
                         nextTimestamp, blockData, difficulty)
    if addBlock(newBlock):
        #broadcastLatest()
        print('broadcastLatest() adding: ' + json.dumps(newBlock.__dict__))
    return newBlock

def generateNextBlock(blockData):
    coinbaseTx = getCoinbaseTransaction(getPublicFromWallet(), getLatestBlock().index + 1)
    blockData = [coinbaseTx].concat(getTransactionPool())
    return generateRawNextBlock(blockData)


def isValidNewBlock(newBlock, previousBlock):
    if not isValidBlockStructure(newBlock):
        print('invalid structure')
        return False
    elif previousBlock.index + 1 != newBlock.index:
        print('invalid index')
        return False
    elif previousBlock.hash != newBlock.previousHash:
        print('invalid previoushash')
        return False
    elif not isValidTimestamp(newBlock, previousBlock):
        print('invalid timestamp')
        return False
    elif not hasValidHash(newBlock):
        return False
    # change newBlock to newBlock.__dict__?
    return True

def hasValidHash(block):
    if not hashMatchesBlockContent(block):
        print('invalid hash, got:' + block.hash)
        return False
    if not hashMatchesDifficulty(block.hash, block.difficulty):
        print('block difficulty not satisfied. Expected: ' + block.difficulty + 'got: ' + block.hash)
        return False
    return True

def hashMatchesBlockContent(block):
    blockHash = calculateHashForBlock(block)
    return blockHash == block.hash

def addBlock(newBlock):
    if isValidNewBlock(newBlock, getLatestBlock()):
        blockchain.append(newBlock)

def isValidBlockStructure(block):
    return (type(block.index) == int and
            type(block.hash) == str and
            type(block.previousHash) == str and
            type(block.timestamp) == int and
            type(block.data) == str)

def isvalidChain(blockchainToValidate):
    #if JSON.stringify(blockchainToValidate[0]) != JSON.stringify(genesisBlock):
    if json.dumps(blockchainToValidate[0]) != json.dumps(getGenesisBlock()):
        return False
    for i in range(1, len(blockchainToValidate)):
        if not isValidNewBlock(blockchainToValidate[i], blockchainToValidate[i - 1]):
            return False
    return True

def replaceChain(newBlocks):
    if (isvalidChain(newBlocks) and 
        getAccumulatedDifficulty(newBlocks) > getAccumulatedDifficulty(getBlockchain())):
        print('Received blockchain is valid. Replacing current blockchain with received blockchain')
        blockchain = newBlocks
        #broadcastLatest()
    print('Received blockchain invalid')

### Blockchain fucntions
def getLatestBlock():
    return getBlockchain()[-1]
def getGenesisBlock():
    return genesisBlock
def getBlockchain():
    return blockchain

###################################################POW

def hashMatchesDifficulty(hash, difficulty):
    hashBinary = bin(int(hash, 16))[2:].zfill(len(hash) * 4)
    requiredPrefix = '0' * difficulty
    return hashBinary.startswith(requiredPrefix)

def findBlock(index, previousHash, timestamp, data, difficulty):
    nonce = 0
    while True:
        hash = calculateHash(index, previousHash,
                             timestamp, data, difficulty, nonce)
        if hashMatchesDifficulty(hash, difficulty):
            return Block(index, hash, previousHash, timestamp, data, difficulty, nonce)
        nonce += 1

def getDifficulty(aBlockchain):
    latestBlock = aBlockchain[-1]
    if latestBlock.index % 10 == 0 and latestBlock.index != 0:
        return getAdjustedDifficulty(latestBlock, aBlockchain)
    else:
        return latestBlock.difficulty

def getAdjustedDifficulty(latestBlock, aBlockchain):
    prevAdjustmentBlock = aBlockchain[-10]
    timeExpected = BLOCK_GENERATION_INTERVAL * 10
    timeTaken = latestBlock.timestamp - prevAdjustmentBlock.timestamp
    if timeTaken < timeExpected / 2:
        return prevAdjustmentBlock.difficulty + 1
    elif timeTaken > timeExpected * 2:
        return prevAdjustmentBlock.difficulty - 1
    else:
        return prevAdjustmentBlock.difficulty

def isValidTimestamp(newBlock, previousBlock):
    # A block is valid, if the timestamp is at most 1 min in the future from the time we perceive.
    # A block in the chain is valid, if the timestamp is at most 1 min in the past of the previous block.
    return (previousBlock.timestamp - 60 < newBlock.timestamp and
            newBlock.timestamp - 60 < getCurrentTimestamp())

def getAccumulatedDifficulty(aBlockchain):
    difficulty = map(lambda block: 2**block.difficulty, aBlockchain)
    return sum(difficulty)



# ------------CHAPTER 5 BLOCKCHAIN.PY----------------
def getUnspentTxOuts():
    return unspentTxOuts[:]

def sendTransaction(address, amount):
    tx = createTransaction(address, amount, getPrivateFromWallet(), unspentTxOuts, transactionPool)
    addToTransactionPool(tx, getUnspentTxOuts())
    # broadCastTransactionPool()
    print('broadcasting transaction: %s' % json.dumps(tx))
    return tx


def handleReceivedTransaction(transaction):
    addToTransactionPool(transaction, getUnspentTxOuts())


###################################################
genesisTransaction = Transaction(
    'e655f6a5f26dc9b4cac6e46f52336428287759cf81ef5ff10854f69d68f43fa3',
    [TxIn('', 0, '')],
    [TxOut('04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a', 50)]
)

genesisBlock = Block(0, '91a73664bc84c0baa1fc75ea6e4aa6d1d20c5df664c724e3159aefc2e1186627',
                     '', 1465154705, [genesisTransaction], 0, 0)

blockchain = [genesisBlock]

unspentTxOuts = processTransactions(blockchain[0].data, [], 0)

BLOCK_GENERATION_INTERVAL = 10  # in seconds

DIFFICULTY_ADJUSTMENT_INTERVAL = 10  # in blocks

# COINBASE_AMOUNT = 50 # in transacion.py

# transactionPool = [] # in transactionPool.py

#######################testing############################
# print(blockchain)
# print(unspentTxOuts)

# generate first key pair
# privateK = initWallet()
# publicK = getPublicFromWallet()

# mining first block

# make first transaction to self
# sign the transaction using private key


# print(blockchain[0].__dict__)
# # first block object
# {
#     'index': 0,
#     'previousHash': '',
#     'timestamp': 1465154705,
#     'data': [ < transaction.Transaction object at 0x7fd8d58e8580 > ],
#     'hash': '91a73664bc84c0baa1fc75ea6e4aa6d1d20c5df664c724e3159aefc2e1186627',
#     'difficulty': 0,
#     'nonce': 0
# }

# print(blockchain[0].data[0].__dict__)
# # first block data (transaction object)
# {
#     'id': 'e655f6a5f26dc9b4cac6e46f52336428287759cf81ef5ff10854f69d68f43fa3',
#     'txIns': [<transaction.TxIn object at 0x7f6a9a209280>],
#     'txOuts': [<transaction.TxOut object at 0x7f6a9a209460>]
# }

# print(blockchain[0].data[0].txIns[0].__dict__)
# {
#     'txOutId': '',
#     'txOutIndex': 0,
#     'signature': ''
# }

# print(blockchain[0].data[0].txOuts[0].__dict__)
# {
#     'address': '04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a',
#     'amount': 50
# }

# print(unspentTxOuts[0].__dict__)
# # first unspentTxOuts object
# {
#     'txOutId': 'e655f6a5f26dc9b4cac6e46f52336428287759cf81ef5ff10854f69d68f43fa3',
#     'txOutIndex': 0,
#     'address': '04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a',
#     'amount': 50
# }
