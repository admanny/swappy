import os
import sys
import yaml
import argparse
import logging

from typing import Dict

from web3 import Web3, types
from pancakeswap_wrapper import utils
from pancakeswap_wrapper.pancakeswap import Pancakeswap


logging.basicConfig(format='%(filename)s:%(levelname)s:%(message)s', level=logging.INFO)
logging.getLogger(__name__)


BNB = "0x0000000000000000000000000000000000000000"

def get_swap_config() -> Dict:
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.yml'))

    with open(config_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except Exception:
            raise Exception
    return config.get('swap')


def parse_args(args):
    """
    Parse the given script arguments and assign them to variables as defined
    in the 'dest' parameter of the `add_argument` method.
    """

    parser = argparse.ArgumentParser(description="CLI tool to swap tokens on pancakeswap",
                                     usage=f'python swap.py --input-token {BNB} --output-token 0x111...01')
            
    parser.add_argument('-i', '--input-token',
                        help="Contract address of token to swap",
                        dest="input_token",
                        default=None)

    parser.add_argument('-o', '--output-token',
                        help="Contract address of desired token to receive as result of swap",
                        dest="output_token",
                        default=None)
    
    parser.add_argument('-qty', '--quantity',
                        help="Quantity of token (use standard decimal representation, i.e., 1 for one input token, 0.5 for half a input token, etc...)",
                        dest="qty",
                        required=True)

    return parser.parse_args(args)


def get_token_decimals(input_token: str, w3: Web3):
    """
    Get decimals from token contract
    """
    if input_token != BNB:
        erc20_contract = utils.load_contract("erc20", input_token, w3)

        token_decimals = erc20_contract.functions.decimals().call()
    else:
        token_decimals = 18 # BNB token
    
    return token_decimals


def main():
    args = parse_args(sys.argv[1:])

    # Get needed attributes from config.yml
    config = get_swap_config()

    network_url = config.get('network_url')
    my_address = config.get('my_address')
    my_pk = config.get('my_pk')
    
    # Create web3 provider
    web3_provider = Web3(Web3.HTTPProvider(network_url))

    input_token = web3_provider.toChecksumAddress(args.input_token)
    output_token = web3_provider.toChecksumAddress(args.output_token)

    # Convert gas for transaction
    gwei = types.Wei(Web3.toWei(int(10), "gwei"))

    # Get token decimals and convert quantity input to wei
    decimals = get_token_decimals(input_token, web3_provider)
    quantity = int(float(args.qty) * float(10 ** decimals))

    try:
        pancakeswap = Pancakeswap(my_address, my_pk, web3=Web3(Web3.HTTPProvider(network_url)), max_slippage=0.15)

    except Exception as e:
        logging.exception("Error initializing Pancakeswap client")
    
    try:
        txnid = pancakeswap.make_trade(input_token, output_token, quantity, gwei, my_address, my_pk)
        tx = web3_provider.eth.wait_for_transaction_receipt(txnid)
        
        status = tx.status
        logging.info(f"Transaction status: {'success' if status == 1 else 'Failed'}")

    except Exception as e:
        logging.exception("Error when swapping tokens")


if __name__ == "__main__":
    main()
