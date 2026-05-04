import calendar
import matplotlib.pyplot as plt

from modules.loader import load_data
from modules.filters import filter_by_month
from modules.analysis import section_wise_data, total_spend, category_spend
from modules.budget import compare_budget

# Load data
df = load_data()

# CLI input
try:
    month = int(input("Enter month (1-12): "))
    year = int(input("Enter year (e.g., 2026): "))
except ValueError:
    print("❌ Please enter valid numbers")
    exit()

if month < 1 or month > 12:
    print("❌ Invalid month. Must be 1–12.")
    exit()

month_name = calendar.month_name[month]
print(f"\n📅 Month: {month_name} {year}")

# Filter data
df_filtered = filter_by_month(df, month, year)
if df_filtered.empty:
    print("⚠️ No data found for this month.")
    exit()

# Analysis
total = total_spend(df_filtered)
needs, wants = section_wise_data(df_filtered)
category = category_spend(df_filtered)
category = category.sort_values(ascending=False)

# Budget (example)
budget = {
    "Food": 8000,
    "Rent": 11000,
    "Shopping": 5000
}

budget_result = compare_budget(category, budget)

# Output (clean format)
print(f"\n📅 Month: {month}/{year}")
print("💰 Total Spend:", total)
print("🟢 Needs:", needs)
print("🟡 Wants:", wants)

print("\n📊 Category Spend:")
print(category)

print("\n📉 Budget Status:")
for cat, data in budget_result.items():
    print(f"{cat}: Spent {data['spent']} | Remaining {data['remaining']}")


print("\n📊 Generating charts...")

# Visualization Category-wise Bar Chart
plt.figure()
category.plot(kind="bar")

plt.title("Category-wise Spending")
plt.xlabel("Category")
plt.ylabel("Amount")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# Visualization Needs vs Wants Pie Chart
if needs + wants > 0:
    plt.figure()
    plt.pie([needs, wants], labels=["Needs", "Wants"], autopct="%1.1f%%", colors=["#4CAF50", "#FFC107"])
    plt.title("Needs vs Wants")
    plt.show()     
else:
    print("⚠️ No spending data to visualize for Needs vs Wants.")