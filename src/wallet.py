from dotcoin import *
import ecdsa
from transaction import *

def getPrivateFromWallet():
    privateKey = None
    try:
        with open(privateKeyLocation, 'r') as f:
            privateKey = f.read()
    except (IOError, IndexError):
        print('no wallet found')
    return privateKey


def getPublicFromWallet():
    privateKey = getPrivateFromWallet()
    key = ecdsa.SigningKey.from_string(
        bytes.fromhex(privateKey), curve=ecdsa.SECP256k1)
    publicKey = key.get_verifying_key().to_string().hex()
    return publicKey


def generatePrivateKey():
    keyPair = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    privateKey = keyPair.to_string().hex()
    return privateKey


def initWallet():
    try:
        with open(privateKeyLocation, 'r') as f:
            privateKey = f.read()
    except (IOError, IndexError):
        privateKey = generatePrivateKey()
        with open(privateKeyLocation, 'w') as f:
            f.write(privateKey)
        print('new wallet with private key created')
    return privateKey

# def deleteWallet():
#     os.remove(privateKeyLocation)


def getBalance(address):
    balance = 0
    uTxOs = findUnspentTxOuts(address, unspentTxOuts)
    for uTxO in uTxOs:
        balance += uTxO.amount
    return balance


def findUnspentTxOuts(ownerAddress, unspentTxOuts):
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
    for myUnspentTxOut in myUnspentTxOuts:
        includedUnspentTxOuts.append(myUnspentTxOut)
        currentAmount += myUnspentTxOut.amount
        if currentAmount >= amount:
            leftOverAmount = currentAmount - amount
            return includedUnspentTxOuts, leftOverAmount
    raise Exception('not enough coins to send transaction')


def createTxOuts(receiverAddress, myAddress, amount, leftOverAmount):
    txOut1 = TxOut(receiverAddress, amount)
    if leftOverAmount == 0:
        return [txOut1]
    else:
        leftOverTx = TxOut(myAddress, leftOverAmount)
        return [txOut1, leftOverTx]

def filterTxPoolTxs(unspentTxOuts, transactionPool):
    txIns = [txIn for tx in transactionPool for txIn in tx.txIns]
    removable = []
    for tx in transactionPool:
        for txIn in tx.txIns:
            uTxOut = findUnspentTxOuts(txIn.txOutId, txIn.txOutIndex, unspentTxOuts)
            if uTxOut == None:
                removable.append(tx)
    return list(filter(lambda tx: tx not in removable, transactionPool))


def createTransaction(receiverAddress, amount, privateKey, unspentTxOuts, txPool):
    print('txPool: ' + txPool)
    myAddress = getPublicKey(privateKey)
    myUnspentTxOutsA = findUnspentTxOuts(myAddress, unspentTxOuts)

    myUnspentTxOuts = filterTxPoolTxs(myUnspentTxOutsA, txPool)

    # filter from unspentOutputs such inputs that are referenced in pool
    (includeUnspentTxOuts, leftOverAmount) = findTxOutsForAmount(
        amount, myUnspentTxOuts)

    def toUnsignedTxIn(unspentTxOut):
        txIn = TxIn()
        txIn.txOutId = unspentTxOut.txOutId
        txIn.txOutIndex = unspentTxOut.txOutIndex
        return txIn

    unsignedTxIns = list(map(toUnsignedTxIn, includeUnspentTxOuts))

    tx = Transaction()
    tx.txIns = unsignedTxIns
    tx.txOuts = createTxOuts(
        receiverAddress, myAddress, amount, leftOverAmount)
    tx.id = getTransactionId(tx)
    tx.txIns = list(map(lambda txIn, index: signTxIn(
        tx, index, privateKey, unspentTxOuts), tx.txIns, range(len(tx.txIns))))
    return tx


# @app.route('/mineTransaction', methods=['POST'])
# def mineTransaction():
#     address = request.form['address']
#     amount = request.form['amount']
#     resp = generatenextBlockWithTransaction(address, amount)
#     return json.dumps(resp)


privateKeyLocation = 'wallet/private_key'