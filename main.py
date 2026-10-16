import argparse
import sys
from tabulate import tabulate
from database import initialize_db, add_expense, get_all_expenses, delete_expense, get_summary

def main():
    initialize_db()

    parser = argparse.ArgumentParser(description="Personal Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount spent")
    add_parser.add_argument("--category", type=str, required=True, help="Category of expense")
    add_parser.add_argument("--description", type=str, required=True, help="Brief description")
    add_parser.add_argument("--date", type=str, help="Date in YYYY-MM-DD format (defaults to today)")

    # List command
    subparsers.add_parser("list", help="List all expenses")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show total spending summary")
    summary_parser.add_argument("--month", type=str, help="Filter by month (MM, e.g., 10 for October)")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.category, args.description, args.date)
        print(f"Expense added: {args.amount} for {args.category}")

    elif args.command == "list":
        expenses = get_all_expenses()
        if not expenses:
            print("No expenses found.")
        else:
            headers = ["ID", "Amount", "Category", "Date", "Description"]
            print(tabulate(expenses, headers=headers, tablefmt="grid"))

    elif args.command == "summary":
        total = get_summary(args.month)
        period = f"for month {args.month}" if args.month else "total"
        print(f"Spending {period}: {total:.2f}")

    elif args.command == "delete":
        if delete_expense(args.id):
            print(f"Expense ID {args.id} deleted successfully.")
        else:
            print(f"Error: Expense ID {args.id} not found.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
