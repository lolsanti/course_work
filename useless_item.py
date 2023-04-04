"""
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
    trader = Trader()
    trader.load_state()

if __name__ == '__main__':
    trader = Trader()
    while True:
        clear_screen()
        print("Current rate:", trader.state['rate'])
        print("USD balance:", trader.state['usd_balance'])
        print("UAH balance:", trader.state['uah_balance'])
        print("Enter command:")
        command = input().strip().lower()
        if command == "quit":
            break
        elif command == "buy":
            print("Enter amount to buy:")
            amount = float(input())
            trader.buy(amount)
        elif command == "sell":
            print("Enter amount to sell:")
            amount = float(input())
            trader.sell(amount)
        elif command == "buy_all":
            trader.buy_all()
        elif command == "sell_all":
            trader.sell_all()
        elif command == "next_rate":
            trader.next_rate()
        else:
            print("Unknown command")
        input("Press Enter to continue...")

"""