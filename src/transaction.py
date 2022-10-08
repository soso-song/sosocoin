import hashlib
import ecdsa
from dotcoin import *
from wallet import *

# ECDSA(Elliptic Curve Digital Signature Algorithm): Public-key cryptography

COINBASE_AMOUNT = 50

class UnspentTxOut:  # uTxO
    def __init__(self, txOutId, txOutIndex, address, amount):
        self.txOutId = txOutId  # txHash
        self.txOutIndex = txOutIndex  # index of the txOut in the tx with txHash
        self.address = address
        self.amount = amount


class TxIn:
    # each txIn refer to an earlier output
    # txIns unlock the coins and the txOuts ‘relock’ the coins
    def __init__(self, txOutId, txOutIndex, signature):
        self.txOutId = txOutId  # txHash
        self.txOutIndex = txOutIndex  # index of the txOut in the tx with txHash
        self.signature = signature  # created by the private-key


class TxOut:
    def __init__(self, address, amount):
        self.address = address  # ECDSA public key
        self.amount = amount


class Transaction:
    def __init__(self, id, txIns, txOuts):
        self.id = id  # txId or txHash
        self.txIns = txIns
        self.txOuts = txOuts


def getTransactionId(transaction):
    txInContent = ''
    # print(transaction.__dict__)
    for txIn in transaction.txIns:
        txInContent += txIn.txOutId + str(txIn.txOutIndex)
    txOutContent = ''
    for txOut in transaction.txOuts:
        txOutContent += txOut.address + str(txOut.amount)
    return hashlib.sha256((txInContent + txOutContent).encode('utf-8')).hexdigest()


def validateTransaction(transaction, aUnspentTxOuts):

    if not isValidTransactionStructure(transaction):
        print('invalid tx structure')
        return False

    if getTransactionId(transaction) != transaction.id:
        print('invalid tx id: ' + transaction.id)
        return False

    hasValidTxIns = True
    for txIn in transaction.txIns:
        if not validateTxIn(txIn, transaction, aUnspentTxOuts):
            print('invalid txIn')
            hasValidTxIns = False
            break

    if not hasValidTxIns:
        print('some of the txIns are invalid in tx: ' + transaction.id)
        return False
    # dont need to check txOuts because they are generated from txIns

    totalTxInValues = sum(map(lambda txIn: getTxInAmount(
        txIn, aUnspentTxOuts), transaction.txIns))
    totalTxOutValues = sum(map(lambda txOut: txOut.amount, transaction.txOuts))

    if totalTxOutValues != totalTxInValues:
        print('totalTxOutValues != totalTxInValues in tx: ' + transaction.id)
        return False

    return True


def validateBlockTransactions(aTransactions, aUnspentTxOuts, blockIndex):
    coinbaseTx = aTransactions[0]
    if not validateCoinbaseTx(coinbaseTx, blockIndex):
        #print('invalid block because coinbase transaction: ' + coinbaseTx.id)
        return False

    # check for duplicate txIns. Each txIn can be included only once
    for tx in aTransactions:
        groups = {}
        for txIn in tx.txIns:
            if txIn.txOutId in groups and txIn.txOutIndex in groups[txIn.txOutId]:
                print('transaction: ' + tx.id + ' has duplicate txIns')
                return False
            else:
                groups[txIn.txOutId] = txIn.txOutIndex

    # all but coinbase transactions
    isValidTransactions = map(validateTransaction, aTransactions, aUnspentTxOuts)
    return all(isValidTransactions)


def validateCoinbaseTx(cbTransaction, blockIndex):
    if cbTransaction == None:
        print('the first transaction in the block must be coinbase transaction')
        return False
    if getTransactionId(cbTransaction) != cbTransaction.id:
        print(getTransactionId(cbTransaction))
        print(cbTransaction.id)
        print('invalid coinbase tx id: ' + cbTransaction.id)
        return False
    if len(cbTransaction.txIns) != 1:
        print('one txIn must be specified in the coinbase transaction')
        return False
    # We will add the block height to input of the coinbase transaction.
    # This is to ensure that each coinbase transaction has a unique txId.
    # Without this rule, for instance,
    # a coinbase transaction stating “give 50 coins to address 0xabc” would always have the same txId.
    # blockIndex is the height of the block
    if cbTransaction.txIns[0].txOutIndex != blockIndex: # genesisTransaction has txOutIndex = '', may cause problem
        print('the txIn signature in coinbase tx must be the block height')
        return False
    if len(cbTransaction.txOuts) != 1:
        print('invalid number of txOuts in coinbase transaction')
        return False
    if cbTransaction.txOuts[0].amount != COINBASE_AMOUNT:
        print('invalid coinbase amount in coinbase transaction')
        return False
    return True


def validateTxIn(txIn, transaction, unspentTxOuts):
    # check txIn exists in unspentTxOuts
    referencedUTxOut = findUnspentTxOut(
        txIn.txOutId, txIn.txOutIndex, unspentTxOuts)
    if referencedUTxOut == None:
        print('referenced txOut not found: id:' +
              txIn.txOutId + ' index:' + txIn.txOutIndex)
        return False
    address = referencedUTxOut.address
    # txOut from unspentTxOuts has wallet address
    # txIn has signature
    # we check if signature is valid using txOut.address
    key = ecdsa.VerifyingKey.from_string(
        bytes.fromhex(address), curve=ecdsa.SECP256k1)
    return key.verify(bytes.fromhex(txIn.signature), bytes.fromhex(transaction.id))


def getTxInAmount(txIn, unspentTxOuts):
    # txIn don't have amount, so we need to find it in unspentTxOuts
    return findUnspentTxOut(txIn.txOutId, txIn.txOutIndex, unspentTxOuts).amount


def findUnspentTxOut(transactionId, index, unspentTxOuts):
    for uTxO in unspentTxOuts:
        if uTxO.txOutId == transactionId and uTxO.txOutIndex == index:
            return uTxO
    return None


def getCoinbaseTransaction(address, blockIndex):
    t = Transaction(
        None,
        [TxIn(None, blockIndex, None)],
        [TxOut(address, COINBASE_AMOUNT)])
    t.id = getTransactionId(t)
    return t


def signTxIn(transaction, txInIndex, privateKey, unspentTxOuts):
    txIn = transaction.txIns[txInIndex]
    txId = transaction.id
    referencedUnspentTxOut = findUnspentTxOut(
        txIn.txOutId, txIn.txOutIndex, unspentTxOuts)
    if referencedUnspentTxOut == None:
        print('could not find referenced txOut from unspentTxOuts')
        # throw Error('could not find referenced txOut')
        return None
    referencedAddress = referencedUnspentTxOut.address
    # check if the private key matches TxOut.address that has TxOut.amount coins from unspentTxOuts(history)
    if getPublicKey(privateKey) != referencedAddress:
        print('trying to sign an input with private' +
              ' key that does not match the address that is referenced in txIn')
        # throw Error()
        return None
    #key = ec.generate_private_key(int(privateKey, 16), ec.SECP256K1())
    #signature = key.sign(dataToSign.encode('utf-8'), ec.ECDSA(hashes.SHA256()))
    key = ecdsa.SigningKey.from_string(
        bytes.fromhex(privateKey), curve=ecdsa.SECP256k1)
    signature = key.sign(bytes.fromhex(txId))

    return signature


def updateUnspentTxOuts(newTransactions, unspentTxOuts):
    # this method is called only after the transactions in the block
    # (and the block itself) has been validated.
    newUnspentTxOuts = []
    consumedTxOuts = []
    # extract all txOuts from newTransactions
    for tx in newTransactions:
        for index, txOut in enumerate(tx.txOuts):
            newUnspentTxOuts.append(
                UnspentTxOut(tx.id, index, txOut.address, txOut.amount)
            )
    # extract all txIns from unspentTxOuts
    for tx in newTransactions:
        for txIn in tx.txIns:
            uTxO = findUnspentTxOut(
                txIn.txOutId, txIn.txOutIndex, unspentTxOuts)
            if uTxO != None:
                consumedTxOuts.append(uTxO)

    # add newUnspentTxOuts from unspentTxOuts
    # remove consumedTxOuts from unspentTxOuts
    resultingUnspentTxOuts = list(
        filter(lambda uTxO: uTxO not in consumedTxOuts, unspentTxOuts)
    )
    resultingUnspentTxOuts = resultingUnspentTxOuts + newUnspentTxOuts

    return resultingUnspentTxOuts


def processTransactions(aTransactions, aUnspentTxOuts, blockIndex):
    if not validateBlockTransactions(aTransactions, aUnspentTxOuts, blockIndex):
        print('invalid block transactions')
        return None
    return updateUnspentTxOuts(aTransactions, aUnspentTxOuts)


def getPublicKey(privateKey):
    #key = ec.generate_private_key(int(privateKey, 16), ec.SECP256K1())
    key = ecdsa.SigningKey.from_string(
        bytes.fromhex(privateKey), curve=ecdsa.SECP256k1)
    return key.public_key().public_numbers().x


def isValidTxInStructure(txIn):
    if txIn == None:
        print('txIn is null')
        return False
    if type(txIn.txOutId) != str:
        print('invalid txIn.txOutId type in transaction')
        return False
    if type(txIn.txOutIndex) != int:
        print('invalid txIn.txOutIndex type in transaction')
        return False
    if type(txIn.signature) != str:
        print('invalid txIn.signature type in transaction')
        return False
    return True


def isValidTxOutStructure(txOut):
    if txOut == None:
        print('txOut is null')
        return False
    if type(txOut.address) != str:
        print('invalid txOut.address type in transaction')
        return False
    if not isValidAddress(txOut.address):
        print('invalid txOut.address in transaction')
        return False
    if type(txOut.amount) != int:
        print('invalid txOut.amount type in transaction')
        return False
    return True

# def isValidTransactionsStructure(transactions):
#     if type(transactions) != list:
#         print('invalid transactions type')
#         return False
#     return map(isValidTransactionStructure, transactions)


def isValidTransactionStructure(transaction):
    if type(transaction.id) != str:
        print('transactionId missing')
        return False
    if type(transaction.txIns) != list:
        print('invalid txIns type in transaction')
        return False
    if not map(isValidTxInStructure, transaction.txIns):
        return False
    if type(transaction.txOuts) != list:
        print('invalid txIns type in transaction')
        return False
    if not map(isValidTxOutStructure, transaction.txOuts):
        return False
    return True


def isValidAddress(address):
    if len(address) != 130:
        print('invalid public key length')
        return False
    if address.match('^[a-fA-F0-9]+$') == None:
        print('public key must contain only hex characters')
        return False
    if address[0:2] != '04':
        print('public key must start with 04')
        return False
    return True

