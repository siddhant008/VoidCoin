from django.http import HttpResponse
import json
from wallet.utils import *
import requests
import pickle
from django.shortcuts import render

# Create your views here.
def new_wallet_form(request):
    return render(request,'wallet/index.html',{})

def new_wallet(request):
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    private_key = sk.to_string().hex()
    vk = sk.get_verifying_key()
    public_key = vk.to_string().hex()
    public_key = base64.b64encode(bytes.fromhex(public_key))
    context = {'private_key': private_key, 'public_key': public_key}
    return HttpResponse(str(context))


def make_transaction(request):
    sender_public_key=request.POST["sender_public"]
    sender_private_key=request.POST["sender_private"]
    reciever_public_key=request.POST["reciever_public"]
    amount=request.POST["amount"]
    if len(sender_private_key == 64):
        signature,message=sign_ECDSA_msg(sender_private_key)

        unverified_transaction = {"from": sender_public_key,
                   "to": reciever_public_key,
                   "amount": amount,
                   "signature": signature.decode(),
                   "message": message}

        pickle.dump('unverified_transactions.dat',unverified_transaction)

    return HttpResponse(str(unverified_transaction))


def check_balance(request):
    public_key=request.POST['public_key']
    blockchain=requests.get('http://localhost:8000/mine_api/show_blockchain')
    balance=0
    for block in blockchain:
        if (block.data['transactions']['sender'] )== public_key:
            balance-=block.data['transactions']['amount']
        else:
            balance += block.data['transactions']['amount']
    context={'balance':balance}
    return HttpResponse(str(context))
