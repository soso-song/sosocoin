from dotcoin import *
from transaction import *
from transactionPool import *

MessageType = {
    "QUERY_LATEST" : 0,
    "QUERY_ALL" : 1,
    "RESPONSE_BLOCKCHAIN" : 2,
    "QUERY_TRANSACTION_POOL" : 3,
    "RESPONSE_TRANSACTION_POOL" : 4
}

responseTransactionPoolMsg = {
    'type': MessageType.RESPONSE_TRANSACTION_POOL,
    'data': json.stringify(getTransactionPool())
}

queryTransactionPoolMsg = {
    'type': MessageType.QUERY_TRANSACTION_POOL,
    'data': None
}

def handleBlockchainResponse(message):
    receivedBlocks = json.loads(message['data'])
    try:
        receivedBlockchain = createBlockchain(receivedBlocks)
        handleBlockchainResponse(receivedBlockchain)
    except:
        print('Invalid blocks received:')
        print(receivedBlocks)

def handleResponseTransactionPool(recievedTransactions):
    for transaction in recievedTransactions:
        try:
            handleReceivedTransaction(transaction)
            broadCastTransactionPool()
        except:
            print('unconfirmed transaction not valid (we probably already have it in our pool)')
    
    

# def initMessageHandler(msg):
#     try:
#         if msg.type == MessageType.QUERY_LATEST:
#             write(ws, responseLatestMsg)
#         elif msg.type == MessageType.QUERY_ALL:
#             write(ws, responseChainMsg)
#         elif msg.type == MessageType.RESPONSE_BLOCKCHAIN:
#             handleBlockchainResponse(msg.data)
#         elif msg.type == MessageType.QUERY_TRANSACTION_POOL:
#             write(ws, responseTransactionPoolMsg)
#         elif msg.type == MessageType.RESPONSE_TRANSACTION_POOL:
#             handleTransactionPoolResponse(msg.data)