# Fetch.ai Auto Compounder Agent

This repository contains a Python script that generates an encryption key and an agent script that uses the encrypted mnemonic phrase. The agent can be run locally or remotely with environment variables. Please be aware that if someone gains access to your environment variables (ENCRYPTION_KEY and ENCRYPTED_SEED), your account could be compromised. As an alternative, you may consider storing these variables in a more secure location.

Agent will automatically select all of your validators, withdraw rewards from them, and stake the INITIAL_STAKE amount on first of them. Staking will only occur if your account balance is greater than or equal to the MINIMUM_ON_ACCOUNT amount. If you don't have a validator yet, make at least one stake manually through your wallet before running script.

## Prerequisites

1. Python 3.6 or higher
2. Install required packages:

   ```bash
   pip install -r requirements.txt


   ```

## Generating Encryption Key and Encrypted Mnemonic Seed

Setup your mnemonic phrase in generate_key.py (!!! Do not commit it !!!):

```bash
# Your mnemonic phrase (replace this with your actual mnemonic phrase)
mnemonic_phrase = b"Your mnemonic phrase here"
```

Run the `generate_key.py` script to generate a unique encryption key and an encrypted mnemonic seed.

```bash
python3 generate_key.py
```

Take note of the output ENCRYPTION_KEY and ENCRYPTED_SEED values. You will use these in the next step.

## Running the Agent Locally

Replace the placeholder values in the agent.py script with your generated ENCRYPTION_KEY and ENCRYPTED_SEED values.

```bash
ENCRYPTION_KEY = "your generated encryption key"
ENCRYPTED_SEED = "your generated encrypted seed"
```

Run the agent.py script:

```bash
python3 agent.py
```

## Remotely

Set the environment variables on your remote server or platform (e.g., Heroku):

```bash
ENCRYPTION_KEY = your generated encryption key
ENCRYPTED_SEED = your generated encrypted seed
```

Deploy and run the agent.py script on your remote server or platform.
Agent Configuration
The agent is designed to be used in a separate thread to avoid blocking the server. It can be run in test mode or main mode, depending on the TEST_MODE variable in the agent.py script.

```bash
TEST_MODE = True # Set to False if you are ready to execute on your main account
```

When running the agent in test mode, it will use the test network configuration. In main mode, it will use the main network configuration.

```bash
ledger = (
LedgerClient(NetworkConfig.fetchai_dorado_testnet())
if TEST_MODE
else LedgerClient(NetworkConfig.fetchai_mainnet())
)
```

You can include this README file in your Git repository to guide users on how to generate the encryption key and run the agent script both locally and remotely. The agent is designed to run in a separate thread, so it won't block the server.
