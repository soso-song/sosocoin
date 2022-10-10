# def init():
#     global genesisTransaction, genesisBlock, blockchain, unspentTxOuts, BLOCK_GENERATION_INTERVAL, DIFFICULTY_ADJUSTMENT_INTERVAL, COINBASE_AMOUNT, transactionPool
    
genesisTransaction = None

genesisBlock = None

blockchain = None

unspentTxOuts = None

BLOCK_GENERATION_INTERVAL = 10  # in seconds

DIFFICULTY_ADJUSTMENT_INTERVAL = 10  # in blocks

COINBASE_AMOUNT = 50

PUBLIC_KEY = None

PRIVATE_KEY = None

transactionPool = None

isMining = False

peers = []
