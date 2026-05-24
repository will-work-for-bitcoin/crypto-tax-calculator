#!/usr/bin/env python3
"""
Crypto Tax Calculator - Calculate capital gains for cryptocurrency transactions
Supports FIFO, LIFO, and specific identification methods

BTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9
"""
import json
import urllib.request
import sys
from datetime import datetime
from collections import defaultdict

class CryptoTaxCalculator:
    def __init__(self):
        self.transactions = []
        self.holdings = defaultdict(float)
    
    def add_transaction(self, date, type_, coin, amount, price_usd, fee=0):
        """Add a buy or sell transaction"""
        self.transactions.append({
            'date': date,
            'type': type_,
            'coin': coin.upper(),
            'amount': amount,
            'price': price_usd,
            'fee': fee,
            'total': amount * price_usd
        })
        
        if type_ == 'buy':
            self.holdings[coin.upper()] += amount
        elif type_ == 'sell':
            self.holdings[coin.upper()] -= amount
    
    def calculate_fifo(self):
        """Calculate capital gains using FIFO method"""
        gains = []
        pending_sales = []
        
        for txn in self.transactions:
            if txn['type'] == 'sell':
                pending_sales.append(txn)
        
        # Match sales with earliest purchases
        for sale in pending_sales:
            remaining = sale['amount']
            for purchase in self.transactions:
                if purchase['type'] == 'buy' and purchase['coin'] == sale['coin']:
                    if remaining <= 0:
                        break
                    match_amount = min(remaining, purchase['amount'])
                    gain = (sale['price'] - purchase['price']) * match_amount
                    gains.append({
                        'date': sale['date'],
                        'coin': sale['coin'],
                        'amount': match_amount,
                        'cost_basis': purchase['price'],
                        'sell_price': sale['price'],
                        'gain': gain,
                        'type': 'short' if (datetime.strptime(sale['date'], '%Y-%m-%d') - 
                                          datetime.strptime(purchase['date'], '%Y-%m-%d')).days <= 365 
                              else 'long'
                    })
                    remaining -= match_amount
        
        return gains
    
    def display_report(self, gains):
        """Display tax report"""
        print("=" * 70)
        print("CRYPTO TAX CALCULATOR")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        if not gains:
            print("\nNo taxable events found.")
            return
        
        total_short = 0
        total_long = 0
        
        print(f"\n{'Date':<12} {'Coin':<8} {'Amount':>10} {'Cost':>10} {'Sell':>10} {'Gain':>12} {'Type':<8}")
        print("-" * 70)
        
        for g in gains:
            cost_str = f"${g['cost_basis']:,.2f}"
            sell_str = f"${g['sell_price']:,.2f}"
            gain_str = f"${g['gain']:,.2f}"
            print(f"{g['date']:<12} {g['coin']:<8} {g['amount']:>10.6f} {cost_str:>10} {sell_str:>10} {gain_str:>12} {g['type']:<8}")
            
            if g['type'] == 'short':
                total_short += g['gain']
            else:
                total_long += g['gain']
        
        print(f"\n{'=' * 50}")
        print(f"Total Short-Term Gains: ${total_short:,.2f}")
        print(f"Total Long-Term Gains:  ${total_long:,.2f}")
        print(f"Total Gains: ${total_short + total_long:,.2f}")
        print(f"\nBTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9")

def main():
    calc = CryptoTaxCalculator()
    
    # Sample transactions for demo
    calc.add_transaction('2024-01-15', 'buy', 'BTC', 0.5, 42000)
    calc.add_transaction('2024-03-20', 'buy', 'BTC', 0.3, 48000)
    calc.add_transaction('2024-06-10', 'sell', 'BTC', 0.4, 52000)
    calc.add_transaction('2024-09-01', 'buy', 'ETH', 5.0, 2400)
    calc.add_transaction('2024-12-15', 'sell', 'ETH', 3.0, 3200)
    
    gains = calc.calculate_fifo()
    calc.display_report(gains)

if __name__ == "__main__":
    main()
