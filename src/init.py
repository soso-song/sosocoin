import config
from blockchain import Block, generateNextBlock
from transaction import Transaction, TxIn, TxOut, processTransactions
from wallet import initWallet

def init():
    config.genesisTransaction = Transaction(
        'e655f6a5f26dc9b4cac6e46f52336428287759cf81ef5ff10854f69d68f43fa3',
        [TxIn('', 0, '')],
        [TxOut('04bfcab8722991ae774db48f934ca79cfb7dd991229153b9f732ba5334aafcd8e7266e47076996b55a14bf9913ee3145ce0cfc1372ada8ada74bd287450313534a', 50)]
    )

    config.genesisBlock = Block(0, '91a73664bc84c0baa1fc75ea6e4aa6d1d20c5df664c724e3159aefc2e1186627',
                        '', 1465154705, [config.genesisTransaction], 0, 0)

    config.blockchain = [config.genesisBlock]

    config.unspentTxOuts = processTransactions(config.blockchain[0].data, [], 0)

    config.BLOCK_GENERATION_INTERVAL = 10  # in seconds

    config.DIFFICULTY_ADJUSTMENT_INTERVAL = 10  # in blocks

    config.COINBASE_AMOUNT = 50

    config.transactionPool = []

    config.isMining = False

    config.PUBLIC_KEY = None

    config.PRIVATE_KEY = None

    initWallet()
    # generateNextBlock()

# def startMining():
#     if config.isMining:
#         findBlock()

