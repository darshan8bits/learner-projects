import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

print("############### Welcome to Personal Expense Analyzer ###############")

categories = ["empty", "Food", "Travel", "Shopping", "Bills", "Others"]
FILE = Path("data.csv")

# Made a different function to load the csv whenever called
# Also cleans irrelevant rows like having NA
# Loading + Data-cleaning

def load_data():
    df = pd.read_csv(FILE)

    df["date"] = pd.to_datetime(
        df["date"], format="%d-%m-%Y", errors="coerce"
    )

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(subset=["date", "amount"])

    return df

# divided the analysis portion into two parts, one non-graphical and the other graphical

def monthly_report(df):

    today = pd.Timestamp.today().normalize()
    current_month = today.month
    current_year = today.year

    start_date = today.replace(day=1)

    current = df[
        (df["date"] >= start_date) &
        (df["date"] <= today)
    ].copy()

    print("\n========== MONTHLY EXPENSE REPORT ==========")
    print(f"Month: {today.strftime('%B %Y')}")

    if current.empty:
        print("No expenses recorded this month.")
    else:
        total = current["amount"].sum()

        # average of transaction for each day
        daily = current.groupby(current["date"].dt.normalize())[
            "amount"
        ].sum().sort_index()

        # Average over this month
        elapsed_days = today.day
        daily_average = total / elapsed_days

        highest_day = daily.idxmax()
        lowest_day = daily.idxmin()

        largest_index = current["amount"].idxmax()
        largest_expense = current.loc[largest_index]

        print(f"\nTotal spending: Rs. {total:.2f}")
        print(f"Daily average: Rs. {daily_average:.2f}")
        print(f"Total transactions: {len(current)}")
        print(f"Days with expenses: {len(daily)}")
        print(
            f"Average transaction: Rs. "
            f"{current['amount'].mean():.2f}"
        )

        print(
            f"\nHighest spending day: "
            f"{highest_day.strftime('%d-%m-%Y')} "
            f"(Rs. {daily.max():.2f})"
        )

        print(
            f"Lowest spending day with an expense: "
            f"{lowest_day.strftime('%d-%m-%Y')} "
            f"(Rs. {daily.min():.2f})"
        )

        print("\nLargest individual expense:")
        print(f"Amount: Rs. {largest_expense['amount']:.2f}")
        print(f"Category: {largest_expense['category']}")
        print(f"Notes: {largest_expense['notes']}")

        print("\nSpending by category:")
        category_totals = current.groupby("category")[
            "amount"
        ].sum().sort_values(ascending=False)

        print(category_totals.to_string())

        if not category_totals.empty:
            print(
                f"\nHighest spending category: "
                f"{category_totals.idxmax()}"
            )

    # Comparison with the previous month
    previous_month_end = start_date - pd.Timedelta(days=1)
    previous_month_start = previous_month_end.replace(day=1)

    comparison_end = min(
        previous_month_end,
        previous_month_start + pd.Timedelta(days=today.day - 1)
    )

    previous = df[
        (df["date"] >= previous_month_start) &
        (df["date"] <= comparison_end)
    ]

    current_total = current["amount"].sum()
    previous_total = previous["amount"].sum()

    print("\n========== PREVIOUS MONTH COMPARISON ==========")
    print(
        f"Current month so far: Rs. {current_total:.2f}"
    )
    print(
        f"Previous month, comparable days: "
        f"Rs. {previous_total:.2f}"
    )

    difference = current_total - previous_total

    if previous_total != 0:
        percentage = difference / previous_total * 100

        if difference > 0:
            print(f"Spending increased by Rs. {difference:.2f} "
                  f"({percentage:.2f}%).")
        elif difference < 0:
            print(f"Spending decreased by Rs. {-difference:.2f} "
                  f"({-percentage:.2f}%).")
        else:
            print("Spending is unchanged.")
    else:
        print("Percentage comparison unavailable: previous spending is zero.")


# Pie chart for selected month
# for showing total expenditure by category

def category_pie_chart(df):

    month = int(input("Enter month number (1-12): "))
    year = int(input("Enter year: "))

    if month < 1 or month > 12:
        print("Invalid month number.")
        return

    selected = df[
        (df["date"].dt.month == month) &
        (df["date"].dt.year == year)
    ]

    if selected.empty:
        print("No expenses found for the entered month.")
        return

    # Include all five categories
    # Replacing absent values with amount = 0
    
    totals = (
        selected.groupby("category")["amount"]
        .sum()
        .reindex(categories[1:], fill_value=0)
    )

    totals = totals[totals > 0]

    plt.figure(figsize=(8, 8))
    plt.pie(
        totals,
        labels=totals.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title(f"Expense Breakdown - {pd.Timestamp(year=year, month=month, day=1).strftime('%B %Y')}")
    plt.tight_layout()
    plt.show()
    plt.close()


# Monthly chart

def yearly_bar_chart(df):

    year = pd.Timestamp.today().year

    yearly = df[df["date"].dt.year == year]

    monthly = (
        yearly.groupby(yearly["date"].dt.month)["amount"]
        .sum()
        .reindex(range(1, 13), fill_value=0)
    )

    month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    plt.figure(figsize=(11, 6))
    plt.bar(month_names, monthly.values)

    plt.title(f"Monthly Spending - {year}")
    plt.xlabel("Month")
    plt.ylabel("Total spending (Rs.)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()
    plt.close()



# Current month vs previous month line chart

def comparative_line_chart(df):

    today = pd.Timestamp.today().normalize()
    current_start = today.replace(day=1)
    previous_end = current_start - pd.Timedelta(days=1)
    previous_start = previous_end.replace(day=1)

    current = df[
        (df["date"] >= current_start) &
        (df["date"] <= today)
    ]

    previous = df[
        (df["date"] >= previous_start) &
        (df["date"] <= previous_end)
    ]

    if current.empty and previous.empty:
        print("No expenses recorded in either month.")
        return

    current_daily = current.groupby(
        current["date"].dt.day
    )["amount"].sum()

    previous_daily = previous.groupby(
        previous["date"].dt.day
    )["amount"].sum()

    # Align both series by day number, filling missing days with zero
    days = range(1, max(today.day, previous_end.day) + 1)

    current_daily = current_daily.reindex(days, fill_value=0)
    previous_daily = previous_daily.reindex(days, fill_value=0)

    plt.figure(figsize=(11, 6))

    plt.plot(
        list(days), current_daily.values,
        marker="o", label=today.strftime("%B")
    )

    plt.plot(
        list(days), previous_daily.values,
        marker="o", label=previous_start.strftime("%B")
    )

    plt.title("Daily Spending Comparison")
    plt.xlabel("Day of the month")
    plt.ylabel("Spending (Rs.)")
    plt.xticks(range(1, 32))
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

while True:

    print("\nThese are your options:")
    print("1. Add Expense")
    print("2. View Expense")
    print("3. Analyze Expenses")
    print("4. Exit")

    try:
        c1 = int(input("Enter your choice >>> "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if c1 == 1:

        try:
            amount = float(input("Enter the amount >>> "))
            if amount < 0:
                print("Amount cannot be negative.")
                continue

            date = input("Enter the date (dd-mm-yyyy) >>> ")
            pd.to_datetime(date, format="%d-%m-%Y")

            print("1. Food")
            print("2. Travel")
            print("3. Shopping")
            print("4. Bills")
            print("5. Others")

            cat = int(input("Enter your choice >>> "))

            if cat not in range(1, 6):
                print("Invalid category.")
                continue

            category = categories[cat]
            notes = input("Any detail to note down? >>> ")

            # Append a correctly formatted CSV row
            new_row = pd.DataFrame([{
                "date": date,
                "amount": amount,
                "category": category,
                "notes": notes
            }])

            new_row.to_csv(
                FILE,
                mode="a",
                header=not FILE.exists() or FILE.stat().st_size == 0,
                index=False
            )

            print("Expense added successfully!")

        except (ValueError, OSError) as e:
            print(f"Could not add expense: {e}")

    elif c1 == 2:

        try:
            df = load_data()

            print("\n1. View last n expenses")
            print("2. View this week")
            print("3. View this month")
            print("4. View this year")

            c2 = int(input("Enter your choice >>> "))

            if c2 == 1:
                n = int(input("Enter n >>> "))
                print(df.tail(n))

            elif c2 == 2:
                today = pd.Timestamp.today().normalize()
                start_of_week = today - pd.Timedelta(
                    days=today.weekday()
                )

                print(df[
                    (df["date"] >= start_of_week) &
                    (df["date"] <= today)
                ])

            elif c2 == 3:
                today = pd.Timestamp.today()

                print(df[
                    (df["date"].dt.month == today.month) &
                    (df["date"].dt.year == today.year)
                ])

            elif c2 == 4:
                year = pd.Timestamp.today().year
                print(df[df["date"].dt.year == year])

            else:
                print("Invalid choice.")

        except (ValueError, OSError) as e:
            print(f"Could not read expenses: {e}")

    elif c1 == 3:

        try:
            df = load_data()

            print("\n========== ANALYZE EXPENSES ==========")
            print("1. Non-graphical monthly analysis")
            print("2. Graphical analysis")
            analysis_choice = int(input("Enter your choice >>> "))

            if analysis_choice == 1:
                monthly_report(df)

            elif analysis_choice == 2:

                print("\n========== GRAPHICAL ANALYSIS ==========")
                print("1. Category-wise spending (Pie chart)")
                print("2. Month-to-month spending this year (Bar chart)")
                print("3. Current month vs previous month (Line chart)")
                print("4. Back")

                graph_choice = int(input("Enter your choice >>> "))

                if graph_choice == 1:
                    category_pie_chart(df)

                elif graph_choice == 2:
                    yearly_bar_chart(df)

                elif graph_choice == 3:
                    comparative_line_chart(df)

                elif graph_choice == 4:
                    continue

                else:
                    print("Invalid choice.")

            else:
                print("Invalid choice.")

        except (ValueError, OSError, KeyError) as e:
            print(f"Could not analyze expenses: {e}")

    elif c1 == 4:
        print("Thank you for using Personal Expense Analyzer!")
        break

    else:
        print("Invalid choice. Select 1-4.")
