#!/usr/bin/env python
# coding: utf-8
import datetime
import hashlib
import json
import requests
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask,jsonify,request
import Blockchain
blockchain = Blockchain.create_blockchain()
app = Flask(__name__)
node_address = str(uuid4()).replace('-','')

@app.route('/broadcast_chain' , methods = ['POST'])
def broadcast_chain():
    temp_block = request.get_json().get('temp_block')
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    block = {'index' : len(blockchain.chain) +1 ,
            'timestamp' : str(datetime.datetime.now()) ,
            'proof' : temp_block['proof'],
            'previous_hash' : previous_hash,
            'transactions' : temp_block['transactions']}
    blockchain.chain.append(block)
    response = {'message' : f'This transaction will be added to Block '}
    return jsonify(response),201

@app.route('/mine_block' , methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message' : 'Congratulations, You just mined a block!',
               'index' : block['index'],
               'timestamp' : block['timestamp'],
               'proof' : block['proof'],
               'previous_hash' : block['previous_hash'],
               'transactions' : block['transactions']}
    for node in blockchain.nodes:       
        temp_block = {'temp_block':block}
        URL = str('http://')+node+"/broadcast_chain"        
        try:
            _ = requests.post(URL, json=temp_block)
        except:
            pass
    return jsonify(response),200

@app.route('/get_chain' , methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
               'length' : len(blockchain.chain)}
    return jsonify(response),200

@app.route('/is_valid' , methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid == 2:
        response = {'message' : "Your Blockchain is valid!"}
    elif is_valid ==0:
        response = {'message' : "We have a problem! Previous Hash invalid!!!"}
    else:
        response = {'message' : "We have a problem! Proof invalid!!!"}
    return jsonify(response),200

@app.route('/add_transaction' , methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount','category']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of the transactions are missing!',400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'],json['category'])
    response = {'message' : f'This transaction will be added to Block {index}'}
    res = mine_block()
    return jsonify(response),201

@app.route('/connect_node' , methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node",400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message' : 'All the nodes are now connected. The currency contains the following nodes : ',
               'total_nodes' : list(blockchain.nodes)}
    return jsonify(response),201

@app.route('/get_node' , methods = ['GET'])                                                                        
def get_nodes():
    response = {'message' : 'Connected nodes : ',
                'nodes' : list(blockchain.nodes)}
    return jsonify(response),200

@app.route('/replace_chain' , methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message' : "The nodes had different chains, so the chain was replaced by the longest one!",
                   'new_chain' : blockchain.chain}
    else:
        response = {'message' : "All good! the chain is the largest one!",
                   'actual_chain' : blockchain.chain}
    return jsonify(response),200

@app.route('/find_transactions' , methods = ['POST'])
def find_transactions():
    json = request.get_json()
    user = json['user']
    if user is None:
        return "No User",400
    trans = [i['transactions'] for i in blockchain.chain][1:]
    info = []
    for i in trans:
        #print(i[0])
        if i[0]['sender'] == user or i[0]['receiver'] == user:

            info.append(i[0])
    if len(info) == 0:
        
        response = {'message' : 'You Had No Transactions So Far! '}
    else:
        response = {'message' : 'You Did the Following Transactions : ',
               'transactions' : list(info)}
    return jsonify(response),201

app.run(host='0.0.0.0',port = 5001)

