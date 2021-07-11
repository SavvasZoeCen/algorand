#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction

#Connect to Algorand node maintained by PureStake
#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    #Your code here
    
    #Generating an account with genAccount.py, save the mnemonic_secret
    #Funding your account on https://bank.testnet.algorand.network/
    #Check the balance with getBalance.py (optional)
    mnemonic_secret = "range acoustic motor today bomb crunch fan certain filter permit gain exist clutch oval meadow vast slush burger swallow air garden urban zebra about shallow"
    sk = mnemonic.to_private_key(mnemonic_secret)
    pk = mnemonic.to_public_key(mnemonic_secret)
    
    #Pay our account
    txtn = transaction.PaymentTxn(pk, tx_fee, first_valid_round, last_valid_round, gen_hash, receiver_pk, tx_amount)
    signedTxtn = txtn.sign(sk)
    
    #Sending a transaction to the Testnet
    txconf = acl.send_transaction(signedTxtn)
    txid = signedTxtn.transaction.get_txid()
    wait_for_confirmation(acl, txid)

    return pk, txid

# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

