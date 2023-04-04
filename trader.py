"""
import argparse
import json
import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Trader:
    def __init__(self, config_path='config.json', state_path='state.json'):
        self.config = self.read_config(config_path)
        self.state_path = state_path
        self.load_state()

    def read_config(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config

    def load_state(self):
        if not os.path.exists(self.state_path):
            self.state = {
                "rate": self.config['initial_rate'],
                "uah_balance": self.config['initial_uah_balance'],
                "usd_balance": self.config['initial_usd_balance']
            }
        else:
            with open(self.state_path, 'r') as f:
                self.state = json.load(f)

    def save_state(self):
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f)

    def next_rate(self):
        delta = self.config['delta']
        self.state['rate'] += round(random.uniform(-delta, delta), 2)
        self.save_state()

    def buy(self, amount):
        rate = self.state['rate']
        uah_balance = self.state['uah_balance']
        usd_balance = self.state['usd_balance']
        cost = amount * rate

        if cost > uah_balance:
            print("UNAVAILABLE, REQUIRED BALANCE UAH {:.2f}, AVAILABLE {:.2f}".format(cost, uah_balance))
            return

        self.state['uah_balance'] -= cost
        self.state['usd_balance'] += amount
        self.save_state()

    def sell(self, amount):
        rate = self.state['rate']
        uah_balance = self.state['uah_balance']
        usd_balance = self.state['usd_balance']
        revenue = amount / rate

        if amount > usd_balance:
            print("UNAVAILABLE, REQUIRED BALANCE USD {:.2f}, AVAILABLE {:.2f}".format(amount, usd_balance))
            return

        self.state['uah_balance'] += revenue
        self.state['usd_balance'] -= amount
        self.save_state()

    def buy_all(self):
        rate = self.state['rate']
        uah_balance = self.state['uah_balance']
        usd_balance = self.state['usd_balance']
        amount = uah_balance // rate
        self.buy(amount)

    def sell_all(self):
        rate = self.state['rate']
        uah_balance = self.state['uah_balance']
        usd_balance = self.state['usd_balance']
        self.sell(usd_balance)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Currency Trader')
    parser.add_argument('command', choices=['RATE', 'AVAILABLE', 'BUY', 'SELL', 'BUY_ALL', 'SELL_ALL', 'NEXT', 'RESTART'], help='Command to execute')
    parser.add_argument('amount', nargs='?', type=float, help='Amount for BUY or SELL command')
    args = parser.parse_args()

    trader = Trader()
    trader.load_state()

    if args.command == 'RATE':
        print(trader.state['rate'])
    elif args.command == 'AVAILABLE':
        print("UAH balance: {:.2f}\nUSD balance: {:.2f}".format(trader.state['uah_balance'], trader.state['usd_balance']))

    elif args.command == 'BUY':
        if not args.amount:
            print("ERROR: Missing amount argument for BUY command")
            exit(1)
        trader.buy(args.amount)

"""

import argparse
import json
import random
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Trader:
    def __init__(self, config_path='config.json', state_path='state.json'):
        self.config = self.read_config(config_path)
        self.state_path = state_path
        self.load_state()

    def read_config(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config

    def load_state(self):
        if not os.path.exists(self.state_path):
            self.state = {
                "rate": self.config['initial_rate'],
                "uah_balance": self.config['initial_uah_balance'],
                "usd_balance": self.config['initial_usd_balance']
            }
        else:
            with open(self.state_path, 'r') as f:
                self.state = json.load(f)

    def save_state(self):
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f)

    def next_rate(self):
        delta = self.config['delta']
        self.state['rate'] += round(random.uniform(-delta, delta), 2)
        self.save_state()

    def buy(self, amount):
        rate = self.state['rate']
        uah_balance = self.state['uah_balance']
        usd_balance = self.state['usd_balance']
        cost = amount * rate

        if cost > uah_balance:
            print("UNAVAILABLE, REQUIRED BALANCE UAH {:.2f}, AVAILABLE {:.2f}".format(cost, uah_balance))
            return

        self.state['uah_balance'] -= cost
        self.state['usd_balance'] += amount
        self.save_state()

    def sell(self, amount):
        rate = self.state['rate']
        uah_balance = self.state['uah_balance']
        usd_balance = self.state['usd_balance']
        revenue = amount * rate

        if amount > usd_balance:
            print("UNAVAILABLE, REQUIRED BALANCE USD {:.2f}, AVAILABLE {:.2f}".format(amount, usd_balance))
            return

        self.state['uah_balance'] += revenue
        self.state['usd_balance'] -= amount
        self.save_state()

    def buy_all(self):
        rate = self.state['rate']
        uah_balance = self.state['uah_balance']
        usd_balance = self.state['usd_balance']
        amount = uah_balance // rate
        self.buy(amount)

    def sell_all(self):
        rate = self.state['rate']
        uah_balance = self.state['uah_balance']
        usd_balance = self.state['usd_balance']
        self.sell(usd_balance)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Currency Trader')
    parser.add_argument('command',
                        choices=['RATE', 'AVAILABLE', 'BUY', 'SELL', 'BUY_ALL', 'SELL_ALL', 'NEXT', 'RESTART'],
                        help='Command to execute')
    parser.add_argument('--amount', type=float, help='Amount for BUY or SELL command')
    args = parser.parse_args()

    trader = Trader()
    trader.load_state()

    if args.command == 'RATE':
        print(trader.state['rate'])
    elif args.command == 'AVAILABLE':
        print(
            "UAH balance: {:.2f}\nUSD balance: {:.2f}".format(trader.state['uah_balance'], trader.state['usd_balance']))
    elif args.command == 'BUY':
        if args.amount is None:
            print("ERROR: --amount parameter is required for BUY command")
        else:
            trader.buy(args.amount)
    elif args.command == 'SELL':
        if args.amount is None:
            print("ERROR: --amount parameter is required for SELL command")
        else:
            trader.sell(args.amount)
    elif args.command == 'BUY_ALL':
        trader.buy_all()
    elif args.command == 'SELL_ALL':
        trader.sell_all()
    elif args.command == 'NEXT':
        trader.next_rate()
    elif args.command == 'RESTART':
        trader = Trader(config_path='config.json', state_path='state.json')
    else:
        print("ERROR: Invalid command")




