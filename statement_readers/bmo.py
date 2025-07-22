from pathlib import Path
import re
import tempfile

import pandas as pd

from exceptions import InvalidStmtFile


def bmo_credit_csv_loader(filename: Path) -> pd.DataFrame:
    if filename.suffix != ".csv": # only handle csv files
        raise InvalidStmtFile("Not a csv file.")
    
    try:
        with open(filename, mode="r", encoding="utf-8-sig") as stmt_file:
            lines = stmt_file.readlines()
    except Exception as e:
        raise InvalidStmtFile(f"Error reading file: {e}")

    # check file format
    if not re.match(r"^Following data is valid as of \d{14}:$", lines[0].strip()):
        raise InvalidStmtFile()
    
    if lines[1].strip() != "": # second line should be empty
        raise InvalidStmtFile()
    
    if lines[2] != "Item #,Card #,Transaction Date,Posting Date,Transaction Amount,Description\n":
        raise InvalidStmtFile()

    try:
        with tempfile.NamedTemporaryFile(mode="w") as temp_file:
            temp_file.writelines(lines[2:]) # skip the first two rows
            temp_file.flush()
            statement_pd = pd.read_csv(temp_file.name)
        
        # set Transaction Date to datetimestamp
        statement_pd["Transaction Date"] = pd.to_datetime(statement_pd["Transaction Date"], format="%Y%m%d")
        statement_pd["Posting Date"] = pd.to_datetime(statement_pd["Posting Date"], format="%Y%m%d")
        # remove the surrounding "'" from the card number
        statement_pd["Card #"] = statement_pd["Card #"].str.strip("'")
    except Exception as e:
        raise InvalidStmtFile()
    
    # normalize the column names
    normalized_columns = {
        "Card #": "card_num",
        "Transaction Date": "transaction_date",
        "Item #": "item_num",
        "Posting Date": "posting_date",
        "Transaction Amount": "amount",
        "Description": "description"
    }
    return (
        statement_pd
        .rename(columns=normalized_columns)
        .set_index(["card_num", "transaction_date", "item_num"])
    )