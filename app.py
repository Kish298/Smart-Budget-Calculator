import os
import json
import calendar
import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for
from google.oauth2.service_account import Credentials

from modules.loader import load_data
from modules.filters import filter_by_month
from modules.sheets_loader import load_data_from_sheets, load_categories_from_sheets
from modules.analysis import total_spend, section_wise_data, category_spend

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_PATH = BASE_DIR / "config" / "credentials.json"


def _get_gspread_client():
    """Get authorized gspread client using env var or file."""
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    import gspread
    
    # Try environment variable first
    creds_json = os.getenv("GOOGLE_CREDS")
    if creds_json:
        try:
            creds_dict = json.loads(creds_json)
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
            return gspread.authorize(creds)
        except Exception:
            pass
    
    # Fall back to file
    try:
        creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=scope)
        return gspread.authorize(creds)
    except Exception as e:
        raise RuntimeError(f"Could not load Google credentials: {e}")


@app.route("/add", methods=["POST"])
def add_expense():
    client = _get_gspread_client()

    spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/12gW_5E-dc8_t06jHLhiBmeGqRwH0OgOXlpM2XwUrPiI/edit?gid=314051676#gid=314051676")
    worksheet = spreadsheet.worksheet("Form Responses 1")

    # Get form data
    category = request.form.get("category")
    type_ = request.form.get("type")
    date_input = request.form.get("date")
    raw_amount = request.form.get("amount") or "0"
    payment = request.form.get("payment")
    notes = request.form.get("notes")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Normalize date to M/D/YYYY for the sheet
    if date_input:
        date_input = date_input.strip()
        try:
            parsed_date = datetime.datetime.strptime(date_input, "%m-%d-%Y")
        except ValueError:
            try:
                parsed_date = datetime.datetime.strptime(date_input, "%m/%d/%Y")
            except ValueError:
                parsed_date = datetime.datetime.today()
        expense_date = f"{parsed_date.month}/{parsed_date.day}/{parsed_date.year}"
    else:
        today = datetime.date.today()
        expense_date = f"{today.month}/{today.day}/{today.year}"

    # Normalize amount to numeric value
    try:
        amount = round(float(raw_amount), 2)
    except ValueError:
        amount = 0.0

    # Append the new row safely to Form Responses 1
    worksheet.append_row(
        [now, expense_date, category, type_, amount, payment, notes],
        value_input_option="USER_ENTERED",
        insert_data_option="INSERT_ROWS"
    )

    return redirect(url_for("index"))

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_data_from_sheets()
    categories = load_categories_from_sheets()
    payment_methods = sorted(df["Payment"].dropna().unique()) if "Payment" in df.columns else []

    # Default values
    month = 5
    year = 2026

    if request.method == "POST":
        month = int(request.form.get("month"))
        year = int(request.form.get("year"))

    df_filtered = filter_by_month(df, month, year)

    total = total_spend(df_filtered)
    needs, wants, investment, savings = section_wise_data(df_filtered)
    category = category_spend(df_filtered).to_dict()

    return render_template(
            "index.html",
            total=total,
            needs=needs,
            wants=wants,
            investment=investment,
            savings=savings,
            category=category,
            category_labels=list(category.keys()),
            category_values=list(category.values()),
            categories=categories,
            payment_methods=payment_methods,
            month=month,
            month_name=calendar.month_name[month],
            year=year
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)