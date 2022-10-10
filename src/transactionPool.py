from transaction import *
import config


def getTransactionPool():
    return config.transactionPool[:]

def addToTransactionPool(transaction, unspentTxOuts):
    # if not isValidTransactionStructure(transaction):
    #     raise Exception('invalid transaction structure: %s' % transaction)
    # if not isTxInAlreadyInPool(transaction, transactionPool):
    #     transactionPool.append(transaction)
    if not validateTransaction(transaction, unspentTxOuts):
        raise Exception('invalid transaction: ' + transaction)
    if not isValidTxForPool(transaction, getTransactionPool()):
        raise Exception('invalid tx for pool: ' + transaction)
    # print('adding to txPool: ' + str(transaction))
    config.transactionPool.append(transaction)

def isValidTxForPool(tx, transactionPool):
    duplicateTxIns = []
    txIn = tx.txIns
    for poolTx in transactionPool:
        print("-----here-----")
        print(poolTx)
        # print(poolTx[0].__dict__)
        for txPoolIn in poolTx.txIns:
            for txIn in tx.txIns:
                if txPoolIn.txOutIndex == txIn.txOutIndex and txPoolIn.txOutId == txIn.txOutId:
                    duplicateTxIns.append(txIn)
                    print('duplicate txIn: ' + txIn)
                    return False
    return True

def hasTxIn(txIn, unsentTxOuts):
    for uTxO in unsentTxOuts:
        if uTxO.txOutId == txIn.txOutId and uTxO.txOutIndex == txIn.txOutIndex:
            return True
    return False

def updateTransactionPool(unspentTxOuts):
    invalidTxs = []
    for tx in getTransactionPool():
        for txIn in tx.txIns:
            if not hasTxIn(txIn, unspentTxOuts):
                invalidTxs.append(tx)
                break
    if len(invalidTxs) > 0:
        print('removing the following transactions from txPool: ' + str(invalidTxs))
        newPool = []
        for tx in getTransactionPool():
            for invalidTx in invalidTxs:
                if tx.id != invalidTx.id:
                    newPool.append(tx)
        config.transactionPool = newPool