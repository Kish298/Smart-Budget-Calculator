def total_spend(df):
    return df["Amount"].sum()

def section_wise_data(df):
    needs = df[df["Type"] == "Needs"]["Amount"].sum()
    wants = df[df["Type"] == "Wants"]["Amount"].sum()
    investment = df[df["Type"] == "Investment"]["Amount"].sum()
    savings = df[df["Type"] == "Savings"]["Amount"].sum()
    return needs, wants, investment, savings

def category_spend(df):
    return df.groupby("Category")["Amount"].sum()