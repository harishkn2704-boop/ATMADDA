from repo import InMemoryRepo
from service import ATMService, seed_demo

def pick(prompt: str, options):
    print(prompt)
    for idx, item in enumerate(options, 1):
        print(f"{idx}. {item}")
    while True:
        try:
            i = int(input("Select: "))
            if 1 <= i <= len(options):
                return i - 1
        except Exception:
            pass
        print("Invalid choice. Try again.")

def run():
    repo = InMemoryRepo()
    bank, atm, cust, chk, sav = seed_demo(repo)
    svc = ATMService(atm, bank, repo)

    print("=== Welcome to ATM ===")
    user_id = input("Insert card (enter user id: CUST1234): ").strip()
    try:
        customer = svc.insert_card(user_id)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if not svc.validate_pin(customer, int(input("Enter PIN: "))):
        print("Invalid PIN")
        return

    lang_idx = pick("Select language:", ["EN", "HI", "ES"])
    atm.select_language(["EN", "HI", "ES"][lang_idx])

    accounts = svc.list_accounts(customer)
    acc_idx = pick("Select account:", [a.account_number for a in accounts])
    account = accounts[acc_idx]

    while True:
        print("\nOptions:", atm.display_options())
        opt = input("Enter option: ").strip().lower()
        if opt in ("exit", "5"):
            print("Thank you!")
            break
        try:

            if opt in ("withdraw", "1"):

            if opt in ("withdraw", "0"):

                amt = int(input("Amount: "))
                bal, tx = svc.withdraw(account, amt)
                print(tx.print_receipt())
                print(f"New balance: {bal}")

            elif opt in ("deposit", "2"):

            elif opt in ("deposit", "1"):

                amt = int(input("Amount: "))
                bal, tx = svc.deposit(account, amt)
                print(tx.print_receipt())
                print(f"New balance: {bal}")
            elif opt in ("balance", "3"):
                bal, tx = svc.balance(account)
                print(tx.print_receipt())
                print(f"Balance: {bal}")
            elif opt in ("mini statement", "mini", "4"):

            elif opt in ("balance", "2"):
                bal, tx = svc.balance(account)
                print(tx.print_receipt())
                print(f"Balance: {bal}")
            elif opt in ("mini statement", "mini", "3"):

                txs = svc.mini_statement(account, last_n=5)
                print("Last transactions:")
                for t in txs:
                    print(f"- {t.date:%Y-%m-%d %H:%M:%S} {t.type} {t.amount} #{t.receipt_id}")
            else:
                print("Unknown option")
        except Exception as e:
            print(f"Operation failed: {e}")

if __name__ == "__main__":

    run()

    run()

