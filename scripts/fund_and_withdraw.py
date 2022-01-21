from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund():
    fund_me = FundMe[-1]
    Account = get_account()
    entrence_fee = fund_me.getEntranceFee()
    print("The current entry fee is {}".format(entrence_fee))
    print("Funding...")
    fund_me.fund({"from": Account, "value": entrence_fee})


def withdraw():
    fund_me = FundMe[-1]
    Account = get_account()
    print("Withdrawing...")
    fund_me.withdraw({"from": Account})


def main():
    fund()
    withdraw()
