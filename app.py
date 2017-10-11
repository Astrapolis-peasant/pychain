from Blockchain import BlockChain
from flask import Flask, jsonify, request
from uuid import uuid4
from textwrap import dedent

# Instantiate Our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # we must receive the reward for find the proof
    # the sender is 0 to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender=0,
        recipient=node_identifier,
        amount=1,
    )
    # forge the new blockchain by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    print(request)
    print([k for k in required])
    if not all([k in values for k in required]):
        return 'Missing values', 400

    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount']
    )
    response = {
        'message': 'Transaction will be added to Block {}'.format(index)
    }
    return jsonify(response), 201


@app.route('/chain', methods=["GET"])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'lenth': len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
