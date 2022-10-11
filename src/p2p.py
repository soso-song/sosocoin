from dotcoin import *
from transaction import *
from transactionPool import *
import config

def handleBlockchainResponse(receivedBlocks):
    result = []
    if len(receivedBlocks) == 0:
        result.append('received block chain size of 0')
        return
    latestBlockReceived = receivedBlocks[-1]
    if not isValidBlockStructure(latestBlockReceived):
        result.append('block structuture not valid')
        return
    latestBlockHeld = getLatestBlock()
    print("---here---")
    print(latestBlockHeld)
    print(latestBlockReceived)

    if latestBlockReceived.__dict__['index'] > latestBlockHeld.__dict__['index']:
        result.append('blockchain possibly behind. We got: ' + str(latestBlockHeld.__dict__['index']) + ' Peer got: ' + str(latestBlockReceived.__dict__['index']))
        if latestBlockHeld.__dict__['hash'] == latestBlockReceived.__dict__['previousHash']:
            if addBlockToChain(latestBlockReceived):
                result.append('block added to chain')
                # broadCast(responseLatestMsg())
            else:
                result.append('block add to chain failed')
        elif len(receivedBlocks) == 1:
            result.append('We have to query the chain from our peer')
            # broadCast(queryAllMsg())
        else:
            result.append('Received blockchain is 2 blocks longer than current blockchain')
            message = replaceChain(receivedBlocks) # contains broadcastLatest()
            result.append(message)
    else:
        result.append('received blockchain is not longer than received blockchain. Do nothing')
    return result

# def handleResponseTransactionPool(recievedTransactions):
#     for transaction in recievedTransactions:
#         try:
#             handleReceivedTransaction(transaction)
#             broadCastTransactionPool()
#         except:
#             print('unconfirmed transaction not valid (we probably already have it in our pool)')
    
    

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