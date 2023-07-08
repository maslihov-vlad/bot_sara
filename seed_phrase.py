from eth_account import Account
from mnemonic import Mnemonic

# Generate a random mnemonic (uses os.urandom(32) to generate 32 random bytes)
def generate_mnemonic():
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)
    return words

# Generate an Ethereum wallet address from a mnemonic
def generate_address(mnemonic):
    # Get the Ethereum account from the mnemonic
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(mnemonic)

    # Get the address associated with the account
    address = account.address

    return address
