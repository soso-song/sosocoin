from transaction import *

transactionPool = []

def getTransactionPool():
    return transactionPool[:]

def addToTransactionPool(transaction, unspentTxOuts):
    # if not isValidTransactionStructure(transaction):
    #     raise Exception('invalid transaction structure: %s' % transaction)
    # if not isTxInAlreadyInPool(transaction, transactionPool):
    #     transactionPool.append(transaction)
    if not validateTransaction(transaction, unspentTxOuts):
        raise Exception('invalid transaction: %s' % transaction)
    if not isValidTxForPool(transaction, unspentTxOuts):
        raise Exception('invalid tx for pool: %s' % transaction)
    print('adding to txPool: %s' % transaction)
    transactionPool.append(transaction)

def isValidTxForPool(tx, transactionPool):
    duplicateTxIns = []
    txIn = tx.txIns
    for txPoolIn in transactionPool.txIns:
        for txIn in tx.txIns:
            if txPoolIn.txOutIndex == txIn.txOutIndex and txPoolIn.txOutId == txIn.txOutId:
                duplicateTxIns.append(txIn)
                print('duplicate txIn: ' + txIn)
                return False
    return True

def hasTxIn(txIns, txIn):
    for txIn in txIns:
        if txIn.txOutId == txIn.txOutId and txIn.txOutIndex == txIn.txOutIndex:
            return True
    return False