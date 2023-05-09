from decimal import Decimal
from colorama import init, Fore
from cosmpy.aerial.client import LedgerClient, NetworkConfig

init(autoreset=True)


class Tools:
    def print_staking_summary(summary, validator_moniker_map):
        print("Staking Summary:")
        print("-" * 40)
        print("Current Positions:")
        for position in summary.current_positions:
            validator = position.validator
            moniker = validator_moniker_map.get(validator, "Unknown")
            amount = Tools.format_balance(position.amount)
            reward = Tools.format_balance(position.reward)
            print(f"  Validator: {validator} ({moniker})")
            print(f"    Amount: {amount}")
            print(f"    Reward: {reward}")
            print()

        print("Unbonding Positions:")
        for position in summary.unbonding_positions:
            validator = position.validator
            moniker = validator_moniker_map.get(validator, "Unknown")
            amount = Tools.format_balance(position.amount)
            print(f"  Validator: {validator} ({moniker})")
            print(f"    Amount: {amount}")
            print()
        print("-" * 40)

    # Common
    @staticmethod
    def print_agent_info(endpoint: str, port: int, address: str, wallet_address: str):
        max_len = 65
        message = f"{Fore.GREEN}" + "+" * max_len + "\n"
        message += f"+\n"
        message += f"+{' '*10}AGENT INFO{' '*10}{Fore.RESET}\n"
        message += f"+\n"
        message += (
            f"+   Endpoint:      {Fore.GREEN}{endpoint.rjust(max_len-30)}{Fore.RESET}\n"
        )
        message += f"+   Port:      {Fore.GREEN}{port}{Fore.RESET}\n"
        message += f"+   Agent address:        {Fore.GREEN}{address.rjust(max_len-32)}{Fore.RESET}\n"
        message += f"+   Agent wallet address: {Fore.GREEN}{wallet_address.rjust(max_len-43)}{Fore.RESET}\n"
        message += f"+\n"
        message += "+" * max_len + f"{Fore.RESET}\n"

        print(message)

    # Ledger and Finance
    @staticmethod
    def format_balance(balance, decimal_places=6):
        fet_balance = Decimal(str(balance))
        sign = ""

        # Check if the balance is negative
        if fet_balance < 0:
            sign = "-"
            fet_balance = abs(fet_balance)

        whole, fractional = divmod(fet_balance, 10**18)
        fractional_str = f"{fractional:018.0f}".rstrip("0")

        # Round
        if len(fractional_str) > decimal_places:
            fractional_str = fractional_str[:decimal_places]

        # Return without zeroes
        if not fractional_str:
            formatted_balance = f"{sign}{whole}"
        else:
            formatted_balance = f"{sign}{whole}.{fractional_str}"

        return formatted_balance
