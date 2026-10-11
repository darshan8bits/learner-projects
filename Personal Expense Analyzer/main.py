import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("############### Welcome to Personal Expense Analyzer ###############")

categories = ["empty", "Food", "Travel", "Shopping", "Bills", "Others"]

while True:
    print("These are your options:")
    print("1. Add Expense")
    print("2. View Expense")
    print("3. Analyze Expenses")

    c1 = int(input("Enter your choice >>> "))

    
    if c1 == 1:
        amount = input("Enter the amount >>> ")
        date = input("Enter the date (dd-mm-yyyy) >>> ")
        print("Enter the category of expense from the five options below: ")
        print("1. Food")
        print("2. Travel")
        print("3. Shopping")
        print("4. Bills (Housing / Electricity / Water / Internet / Gas / Entertainment)")
        print("5. Others")
    
        cat = int(input("Enter your choice >>> "))
        category = categories[cat]
        
        notes = input("Any detail you would like to mark down (< 50 words) >>> ")

        file = open("data.csv", "a")
        file.write(f"{date},{amount},{category},{notes}\n")
        file.close()

        
                      
        
        
    
