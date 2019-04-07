import base64
import hashlib
import time

import ecdsa


class Block:
    def __init__(self,index,timestamp,transaction,previous_hash):
        self.index=index
        self.timestamp=timestamp
        self.transaction=transaction
        self.previous_hash=previous_hash
        self.hash=self.hash_block()

    def hash_block(self):
        sha=hashlib.sha256()
        sha.update((str(self.index)+str(self.timestamp)+str(self.transaction)+str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()


def create_genesis_block():
    return Block(0,time.time(),{"proof-of-work":9,"transactions":None},"0")


def save_blockchain(blockchain):
    with open('blockchain.dat','w') as df:
        df.write(blockchain)
    df.close()

def validate_signature(public_key, signature, message):
    public_key = (base64.b64decode(public_key)).hex()
    signature = base64.b64decode(signature)
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    try:
        return vk.verify(signature, message.encode())
    except:
        return False


def proof_of_work(last_proof, blockchain):
    incrementer = last_proof + 1
    while not (incrementer % 7919 == 0 and incrementer % last_proof == 0):
        incrementer += 1
    return incrementer, blockchain