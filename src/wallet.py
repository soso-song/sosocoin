import ecdsa
# from dotcoin import *
from transaction import TxIn, TxOut, Transaction, getTransactionId, signTxIn
# from blockchain import getUnspentTxOuts
import config

# from config import printTxs 

def generateKeypair():
    privateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    publicKey = privateKey.get_verifying_key()
    return privateKey.to_string().hex(), publicKey.to_string().hex()


def initWallet():
    (privateKey, publicKey) = generateKeypair()
    config.PRIVATE_KEY = privateKey
    config.PUBLIC_KEY = publicKey


def getBalance(address):
    balance = 0
    uTxOs = findUnspentTxOuts(address, config.unspentTxOuts[:])
    for uTxO in uTxOs:
        balance += uTxO.amount
    return balance


def findUnspentTxOuts(ownerAddress, unspentTxOuts):
    # print("------hsfdr-----")
    # print(ownerAddress)
    # print(unspentTxOuts[0].__dict__)
    return list(filter(lambda uTxO: uTxO.address == ownerAddress, unspentTxOuts))
# def findUnspentTxOuts(ownerAddress, unspentTxOuts):
#     uTxOs = []
#     for unspentTxOut in unspentTxOuts:
#         if unspentTxOut.address == ownerAddress:
#             uTxOs += unspentTxOut
#     return uTxOs


def findTxOutsForAmount(amount, myUnspentTxOuts):
    currentAmount = 0
    includedUnspentTxOuts = []
    # print("------here working------")
    # print(amount)
    # print(myUnspentTxOuts)
    for myUnspentTxOut in myUnspentTxOuts:
        includedUnspentTxOuts.append(myUnspentTxOut)
        currentAmount += myUnspentTxOut.amount
        if currentAmount >= amount:
            leftOverAmount = currentAmount - amount
            return includedUnspentTxOuts, leftOverAmount
    raise Exception('not enough coins to send transaction')


def createTransaction(receiverAddress, amount, privateKey, unspentTxOuts, txPool):
    # print('txPool: ' + txPool)
    myAddress = config.PUBLIC_KEY
    myUnspentTxOutsAll = findUnspentTxOuts(myAddress, unspentTxOuts)
    # print("------here wor-----")
    # print(myUnspentTxOutsAll)
    # print("------myUnspentTxOutsAll[0].__dict-----")
    # print(myUnspentTxOutsAll[0].__dict__)
    # filter from unspentOutputs such inputs that are referenced in pool
    myUnspentTxOuts = filterTxPoolTxs(myUnspentTxOutsAll, txPool)
    # print("------here w-----")
    # print(myUnspentTxOuts)

    # filter from unspentOutputs such inputs that are referenced in pool
    (includeUnspentTxOuts, leftOverAmount) = findTxOutsForAmount(amount, myUnspentTxOuts)
    # print("------hfdsfs")
    # print(includeUnspentTxOuts)
    # print(leftOverAmount)

    def toUnsignedTxIn(unspentTxOut):
        txIn = TxIn(unspentTxOut.txOutId, unspentTxOut.txOutIndex, '')
        return txIn

    unsignedTxIns = list(map(toUnsignedTxIn, includeUnspentTxOuts))
    # print("------hfddsfsf22s")
    # print(unsignedTxIns)
    
    
    txIns = unsignedTxIns
    txOuts = createTxOuts(
        receiverAddress, myAddress, amount, leftOverAmount)
    tx = Transaction('', txIns, txOuts)
    tx.id = getTransactionId(tx)
    
    print("ourrange-----------------")
    printTxs([tx])

    # for txIn in tx.txIns:
    for index, txIn in enumerate(tx.txIns):
        print(txIn.__dict__)
        txIn.signature = signTxIn(tx, index, privateKey, unspentTxOuts)

    return tx


def filterTxPoolTxs(unspentTxOuts, transactionPool):
    filUnspentTxOuts = unspentTxOuts[:]
    for tx in transactionPool:
        for txIn in tx.txIns:
            for unspentTxOut in filUnspentTxOuts:
                if unspentTxOut.txOutId == txIn.txOutId and unspentTxOut.txOutIndex == txIn.txOutIndex:
                    filUnspentTxOuts.remove(unspentTxOut)
    return filUnspentTxOuts


def createTxOuts(receiverAddress, myAddress, amount, leftOverAmount):
    txOut1 = TxOut(receiverAddress, amount)
    if leftOverAmount == 0:
        return [txOut1]
    else:
        leftOverTx = TxOut(myAddress, leftOverAmount)
        return [txOut1, leftOverTx]

# privateKeyLocation = 'wallet/private_key'

# def getPrivateFromWallet():
#     privateKey = None
#     try:
#         with open(privateKeyLocation, 'r') as f:
#             privateKey = f.read()
#     except (IOError, IndexError):
#         print('no wallet found')
#     return privateKey

# def getPublicFromWallet():
#     privateKey = getPrivateFromWallet()
#     key = ecdsa.SigningKey.from_string(
#         bytes.fromhex(privateKey), curve=ecdsa.SECP256k1)
#     publicKey = key.get_verifying_key().to_string().hex()
#     return publicKey

# never expect to receive a private key from outside
# def getPublicKey(privateKey):
#     key = ecdsa.SigningKey.from_string(
#         bytes.fromhex(privateKey), curve=ecdsa.SECP256k1)
#     publicKey = key.get_verifying_key().to_string().hex()
#     return publicKey

# def initWallet():
#     try:
#         with open(privateKeyLocation, 'r') as f:
#             privateKey = f.read()
#     except (IOError, IndexError):
#         privateKey = generatePrivateKey()
#         with open(privateKeyLocation, 'w') as f:
#             f.write(privateKey)
#         print('new wallet with private key created')
#     return privateKey

# def deleteWallet():
#     os.remove(privateKeyLocation)



def printTxs(txs):
    print("printTxs-----------------")
    transactions = [tx.__dict__.copy() for tx in txs[:]]
    for transaction in transactions:
        transaction['txIns'] = [txIn.__dict__.copy() for txIn in transaction['txIns']]
        transaction['txOuts'] = [txOut.__dict__ .copy()for txOut in transaction['txOuts']]
    print(transactions)
