import os
from cryptography.fernet import Fernet

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig

from lab_agent import LabAgent

# Set False if you are ready to execute on your main account
TEST_MODE = True

# Default
agent_name = "agentslabautocompounder"
agent_seed = os.environ.get(
    "AGENT_SEED_PHRASE", "agentslabautocompounder"
)  # not important
agent_endpoint = os.environ.get("AGENT_ENDPOINT", "http://127.0.0.1:8001/submit")
agent_port = int(os.environ.get("PORT", 8001))

# Optional
# Stake amount each time you have money
INITIAL_STAKE = os.environ.get("INITIAL_STAKE", 1000000000000000000)
# Minimum amount to have on account to make staking
MINIMUM_ON_ACCOUNT = os.environ.get("MINIMUM_ON_ACCOUNT", 1000000000000000000)

# MUST BE SET
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY", "[generated encryption key]")
ENCRYPTED_SEED = os.environ.get(
    "ENCRYPTED_SEED",
    "[generated encryption seed key]",
)

# Prepare ledger
ledger = (
    LedgerClient(NetworkConfig.fetchai_dorado_testnet())
    if TEST_MODE
    else LedgerClient(NetworkConfig.fetchai_mainnet())
)

# Decorated agent
agent = LabAgent(
    name=agent_name,
    port=agent_port,
    seed=agent_seed,
    endpoint=[agent_endpoint],
    initial_stake=INITIAL_STAKE,
    minimum_on_account=MINIMUM_ON_ACCOUNT,
    encryption_key=ENCRYPTION_KEY,
    encrypted_seed=ENCRYPTED_SEED,
    ledger=ledger,
)

# Give some test money to agent as soon as he will be registered in test net.
# In order to execute code for compounding in main net we don`t need agent to be in main net itself
agent.fund()
agent.print_info()

if __name__ == "__main__":
    agent.run_agent()
