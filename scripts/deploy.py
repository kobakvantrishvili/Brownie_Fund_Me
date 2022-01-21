from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
)


def deploy_fund_me():
    Account = get_account()
    # if we choose to not deploy on development or on ganache-local network do the following
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    # else do the following
    else:
        # deploy our version of price feed contract - known as "Mocking"
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # pass the price feed address to fund_me contract
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": Account},
        publish_source=config["networks"][network.show_active()][
            "verify"
        ]  # or .get("verify") - added in brownie-config.yaml file
        # to Verify & Publish Contract Source Code on EtherScan when network is non-development network like rinkeby
        # we added ETHERSCAN_TOKEN in .env
    )
    # Code Flattening is replacing the imports with the actual code
    print(f"contract deployed to {fund_me.address}")
    # "brownie run scripts/deploy.py --network rinkeby"
    # to deploy to rinkeby network (Infura)

    # if we want to deploy on the ganache chain and we want brownie
    # to remmember our deployment, we have to manually add network
    # "brownie networks add Ethereum {name} host={RPC server host} chainid={Network ID}"
    # in our case:
    # "brownie networks add Ethereum ganache-local host=http://127.0.0.1:8545 chainid=1337"
    # now to deploy at our network we write:
    # "brownie run scripts/deploy.py --network ganache-local"
    return fund_me  # for tests


def main():
    deploy_fund_me()
