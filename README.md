# swappy
Script that executes swaps using Pancakeswap on BSC. This is an early version of the script - there are a variety of improvements that can be made to make the script much more reliable, robust, and user friendly.  


**Usage:**
* Populate `config.yml` with:
    * `network_url`: Currently set to localhost as this has only been tested on a local fork of BSC using ganache.
    * `my_pk`: Your private key
    * `my_address`: Your wallet address
**Note**: If using Ganache to create a local chain instance you can use the address and private key pairs that it provides on start up to test.


**Examples:**

Swap 1 BNB for USDC
```
python swap.py -i 0x0000000000000000000000000000000000000000 -o 0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d -q 1 
```

Swap 10 USDC for BNB
```
python swap.py -i 0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d -o 0x0000000000000000000000000000000000000000 -q 10
```

