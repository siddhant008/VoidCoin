import requests
from miner.utils import *
import pickle
from django.http import HttpResponse

# Create your views here.
def mine(request):
    blockchain = requests.get('http://localhost:8000/mine_api/show_blockchain')
    miner_public_key=request.GET['pkey']
    if(len(blockchain.text)==0):
        save_blockchain([create_genesis_block()])

    transaction=pickle.load('C:/Users/hp/Desktop/voidcoin/unverified_transactions.dat')

    validate_signature(transaction['front'],transaction['signature'],transaction['message'])

    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof,blockchain)

    # Empty transaction list
    NODE_PENDING_TRANSACTIONS = []

    NODE_PENDING_TRANSACTIONS.append({
        "from": "network",
        "to": miner_public_key,
        "amount": 5})

    new_block_data = {
        "proof-of-work": proof[0],
        "transactions": list(NODE_PENDING_TRANSACTIONS)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = time.time()
    last_block_hash = last_block.hash

    # Now create the new block
    mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
    blockchain.append(mined_block)
    with open("C:/Users/hp/Desktop/voidcoin/blockchain.dat",'wb') as df:
        df.write(blockchain)
    df.close()

    return HttpResponse(str(blockchain))


def show_blockchain(request):
    blockchain=pickle.load("blockchain.dat")
    return HttpResponse(str(blockchain))