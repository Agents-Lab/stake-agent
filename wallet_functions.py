import os
import time
import pickle
from cryptography.fernet import Fernet
from cosmpy.aerial.wallet import LocalWallet

from tools import Tools


class Wallet:
    def __init__(
        self, initial_stake, minimum_on_account, encryption_key, encrypted_seed, ledger
    ):
        # validators cache
        self.validators_filename = "validators.pkl"

        # vars for wallet
        self.initial_stake = initial_stake
        self.minimum_on_account = minimum_on_account
        self.encryption_key = encryption_key
        self.encrypted_seed = encrypted_seed

        # self.seed = "dress dress endorse asthma body key lyrics stand flavor mosquito arctic match"
        self.seed = self.encrypt_seed()
        self.account = LocalWallet.from_mnemonic(self.seed)
        self.ledger = ledger

    def save_validators_to_file(
        self,
        validators,
    ):
        with open(self.validators_filename, "wb") as f:
            pickle.dump(validators, f)

    def load_validators_from_file(self):
        with open(self.validators_filename, "rb") as f:
            validators = pickle.load(f)
        return validators

    def get_validators(self):
        if os.path.exists(self.validators_filename):
            validators = self.load_validators_from_file()
        else:
            validators = self.ledger.query_validators()
            self.save_validators_to_file(validators)

        return validators

    def check_balance(self):
        wallet_balance = self.ledger.query_bank_balance(self.account.address())
        balances = self.ledger.query_bank_all_balances(self.account.address())

        # show all coin balances
        for coin in balances:
            balance = Tools.format_balance(coin.amount)
            print(f"{balance} {coin.denom}")

        return wallet_balance

    def delegate_initial_tokens(self, validator_address):
        tx = self.ledger.delegate_tokens(
            validator_address, self.initial_stake, self.account
        )
        tx.wait_to_complete()

    def stake_rewards_once(self, validator_address):
        print("stake_rewards once")

        summary = self.ledger.query_staking_summary(self.account.address())
        print(f"Staked: {Tools.format_balance(summary.total_staked)}")

        balance_before = self.ledger.query_bank_balance(self.account.address())

        print(f"Balance before = {Tools.format_balance(balance_before)}")

        time.sleep(1)
        print("Claiming rewards...")
        tx = self.ledger.claim_rewards(validator_address, self.account)
        print("Complete")
        print("Waiting for transaction complete...")
        tx.wait_to_complete()
        print("Complete")

        balance_after = self.ledger.query_bank_balance(self.account.address())
        print(f"Balance after = {Tools.format_balance(balance_after)}")

        true_reward = balance_after - balance_before
        if true_reward > 0:
            print(f"True_reward = {Tools.format_balance(true_reward)}")
            print(f"Staking {Tools.format_balance(true_reward)} (reward after fees)")

            tx = self.ledger.delegate_tokens(
                validator_address, true_reward, self.account
            )
            tx.wait_to_complete()
            print("tx has been completed")
        else:
            print("Fees from claim rewards transaction exceeded reward")

    def encrypt_seed(self):
        if self.encryption_key is None or self.encrypted_seed is None:
            raise Exception("Ensure you have set environment variables for keys")

        cipher_suite = Fernet(self.encryption_key)
        return cipher_suite.decrypt(self.encrypted_seed.encode()).decode()

    def stake(self, validator_address: str):
        print("Trying to delegate staking to validator...")
        try:
            wallet_balance = self.check_balance()
            print(f"Initial stake - {Tools.format_balance(self.initial_stake)}")

            min = self.initial_stake + self.minimum_on_account
            if wallet_balance < min:
                print(
                    f"Not enough money to stake. Balance = {Tools.format_balance(wallet_balance)}. Needed - {Tools.format_balance(min)}"
                )
            else:
                print(
                    f"We have enough money {Tools.format_balance(wallet_balance)} - trying to stake..."
                )
                self.delegate_initial_tokens(validator_address)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print(f"Error occurred: {e.__class__.__name__} - {e.args}")

    def rewards(self, validator_address: str):
        print("Trying to claim rewards...")
        try:
            self.stake_rewards_once(validator_address)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print(f"Error occurred: {e.__class__.__name__} - {e.args}")

    def get_validators_moniker_map(self, validators):
        return {validator.address: validator.moniker for validator in validators}

    def execute(self):
        validators = self.get_validators()
        validator_moniker_map = self.get_validators_moniker_map(validators)

        print(f"Query summary for account {self.account.address()}")
        summary = self.ledger.query_staking_summary(self.account.address())
        if not summary:
            print("You don`t have validators. Stake them manually first")
            return

        Tools.print_staking_summary(summary, validator_moniker_map)

        for position in summary.current_positions:
            print("Pause before launch on 5 sec...")
            time.sleep(5)
            print("Go...")

            validator = position.validator
            moniker = validator_moniker_map.get(validator, "Unknown")
            amount = Tools.format_balance(position.amount)
            reward = Tools.format_balance(position.reward)
            print(f"  Validator: {validator} ({moniker})")

            print(f"staking for validator {moniker}...")
            self.stake(validator)

            print("Pause between stake and rewards 2 sec...")
            time.sleep(2)

            print(f"rewards for validator {moniker}...")
            self.rewards(validator)

            print("complete")
