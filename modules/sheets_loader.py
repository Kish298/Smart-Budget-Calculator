import gspread
import pandas as pd
import os
import json
from google.oauth2.service_account import Credentials
from modules.loader import load_data

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/12gW_5E-dc8_t06jHLhiBmeGqRwH0OgOXlpM2XwUrPiI/edit?usp=sharing"


def _get_credentials():
    """Load credentials from environment variable or file."""
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Try environment variable first
    creds_json = os.getenv("GOOGLE_CREDS")
    if creds_json:
        try:
            creds_dict = json.loads(creds_json)
            return Credentials.from_service_account_info(creds_dict, scopes=scope)
        except Exception:
            pass
    
    # Fall back to file
    try:
        return Credentials.from_service_account_file(
            "config/credentials.json", scopes=scope
        )
    except Exception:
        raise RuntimeError("Could not load Google credentials from GOOGLE_CREDS env or config/credentials.json")


def _open_spreadsheet():
    creds = _get_credentials()
    client = gspread.authorize(creds)
    return client.open_by_url(SPREADSHEET_URL)


def load_data_from_sheets():
    try:
        spreadsheet = _open_spreadsheet()
        worksheet = spreadsheet.worksheet("Expenses")
        data = worksheet.get_all_records()

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])

        df["Amount"] = (
            df["Amount"]
            .astype(str)
            .str.replace("₹", "", regex=False)
            .str.replace(",", "", regex=False)
        )
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

        return df
    except Exception:
        return load_data()


def load_categories_from_sheets():
    try:
        spreadsheet = _open_spreadsheet()
        categories_sheet = spreadsheet.worksheet("Categories")
        data = categories_sheet.get_all_values()

        categories = [
            row[0].strip()
            for row in data[1:]
            if row and row[0].strip()
        ]

        return sorted(set(categories))
    except Exception:
        df = load_data()
        return sorted(df["Category"].dropna().unique())