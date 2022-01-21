from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIROMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

# "brownie test"
def test_can_fund_and_withdraw():
    Account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    # add +100 just if we need little bit more money
    tx1 = fund_me.fund({"from": Account, "value": entrance_fee})
    tx1.wait(1)
    assert fund_me.addressToAmountFunded(Account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": Account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(Account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip(
            "only for local testing!"
        )  # skip if we are not in development oron ganache-local
    Account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()  # this will give us blank random account
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
