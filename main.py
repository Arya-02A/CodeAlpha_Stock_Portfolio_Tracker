import csv
from datetime import datetime

PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "MSFT": 320,
    "GOOG": 145,
    "AMZN": 130
}

def get_user_portfolio():

    portfolio = []

    print("Enter your stock holdings. Type 'done' when finished.\n")

    while True:

        symbol = input("Enter the company symbol : ").strip()

        if symbol.lower() == "done":
            break
        symbol = symbol.upper()

        if symbol not in PRICES:
            print(f"the symbol, '{symbol}' not found!")
            print(f"Available symbols are : {', '.join(PRICES.keys())}")

        else:
        
            qty_str = input(f"Quantity of {symbol} (integer or float): ").strip()
            try:
                qty = float(qty_str)
                if qty < 0:
                    print("  Quantity must be >= 0. Try again.")
                    continue
            except ValueError:
                print("  Invalid quantity. Please enter a number.")
                continue

            portfolio.append((symbol, qty))

            print(f"------------------------------------------\n{qty} Stocks of {symbol} Added Succesfully...\n------------------------------------------\n")

    return portfolio

def calculate_totals(portfolio):
    
    details = []

    total = 0

    for symbol, qty in portfolio:

        price = PRICES[symbol]

        subtotal = price * qty

        total += subtotal

        details.append({
            "symbol" : symbol,
            "price" : price,
            "quantity" : qty,
            "subtotal" : subtotal
        })

    return details, total

def display(details, total):

    print("\nYOUR PORTFOLIO:\n")

    print(f"{'Symbol':<8} {'Price':>10} {'Quantity':>10} {'Subtotal':>12}")
    print("-" * 44)

    for d in details:
        print(f"{d['symbol']:<8} {d['price']:>10} {d['quantity']:>10} {d['subtotal']:>12.2f}")
    
    print("-" * 44)
    print(f"{'TOTAL':<8} {'':>10} {'':>10} {total:>12.2f}\n")

def save_to_csv(details, total, filename):
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["symbol", "price", "quantity", "subtotal"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in details:
            writer.writerow(d)
        # Write total as final row
        writer.writerow({"symbol": "TOTAL", "price": "", "quantity": "", "subtotal": f"{total:.2f}"})

def main():

    print("================================================================================\nSTOCK PORTFOILO TRACKER\n================================================================================")

    portfolio = get_user_portfolio()

    if not portfolio:
        print("\nNo Stocks Entered..Exiting...")
        return
    
    details, total = calculate_totals(portfolio)
    display(details, total)

    save = input("\nDo you want to save results to a csv file? (y/n) : ").strip()

    if save.lower() == "y":

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"portfolio_{ts}.csv"
        save_to_csv(details, total, filename)

        print(f"Saved as '{filename}'")
    else:
        print("Results not saved. Goodbye.")

main()