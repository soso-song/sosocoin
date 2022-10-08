from flask import Flask, request
# from flask_socketio import SocketIO

from blockchain import *

app = Flask(__name__)
app.debug = True

@app.route("/")
def my_index():
    return Flask.render_template('index.html',token="Hello bro")

@app.route('/blocks', methods=['GET'])
def getBlocks():
    result = []
    for block in getBlockchain():
        result.append(block.__dict__)
    return json.dumps(result)

# doesn't make sense
@app.route('/mineBlock', methods=['POST'])
def mineBlock():
    newBlock = generateNextBlock(str(request.data))
    return json.dumps(newBlock.__dict__)

# @app.route('/peers', methods=['GET'])
# def getPeers():
#     #res.send(getSockets().map(( s: any ) => s._socket.remoteAddress + ':' + s._socket.remotePort));
#     return json.dumps(app.socket)

# @app.route('/addPeer', methods=['POST'])
# def addPeer():
#     connectToPeers(request.body.peer)
#     return json.dumps()

@app.route('/sendTransaction', methods=['POST'])
def mineTransaction():
    address = request.form['address']
    amount = request.form['amount']
    resp = generatenextBlockWithTransaction(address, amount)
    return json.dumps(resp)
