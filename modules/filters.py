def filter_by_month(df, month, year):
    return df[
        (df["Date"].dt.month == month) &
        (df["Date"].dt.year == year)
    ]