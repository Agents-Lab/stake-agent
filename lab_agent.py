# we will use thread for compound process in order do not block main thread of web app
import threading

# uagents
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

# custom addition
from tools import Tools
from wallet_functions import Wallet  # rewards, stake


class LabAgent(Agent):
    def __init__(
        self,
        name,
        port,
        seed,
        endpoint,
        initial_stake,
        minimum_on_account,
        encryption_key,
        encrypted_seed,
        ledger,
    ):
        super().__init__(name=name, port=port, seed=seed, endpoint=endpoint)

        self.port = port
        self.endpoint = endpoint

        self.initial_stake = initial_stake
        self.minimum_on_account = minimum_on_account
        self.encryption_key = encryption_key
        self.encrypted_seed = encrypted_seed

        self.ledger = ledger

    def fund(self):
        pass
        # print("Funding agent...")
        # fund_agent_if_low(self.wallet.address())
        # print("Funding complete")

    def run_agent(self):
        @self.on_interval(period=30.0)
        async def execute_compound_process(ctx: Context):
            print("*" * 50)
            print("Executing compound process")
            print("*" * 50)

            wallet = Wallet(
                self.initial_stake,
                self.minimum_on_account,
                self.encryption_key,
                self.encrypted_seed,
                self.ledger,
            )
            wallet_thread = threading.Thread(target=wallet.execute)
            wallet_thread.start()

        self.run()

    def print_info(self):
        Tools.print_agent_info(
            self.endpoint[0], self.port, self.address, self.wallet.address()
        )
