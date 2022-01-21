from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIROMENTS
    ):
        return accounts[0]
        # by default, forked envrioment doesn't come with its own accounts
        # we have to create our own custom mainnet fork:
        # for infura:
        # "brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://mainnet.infura.io/v3/9b8ac960613d4e8c8ca331c82bd92b21' accounts=10 mnemonic=brownie port=8545"
        # for alchemy (preffered):
        # "brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/iMVebpdRq-i7QXx0KPAl4B99tUrGJfP1 accounts=10 mnemonic=brownie port=8545"
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    # deploy our version of price feed contract - known as "Mocking"
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    # only deploy once
    if len(MockV3Aggregator) <= 0:  # as MockV3Aggregator is list of all deplyements
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed!")
