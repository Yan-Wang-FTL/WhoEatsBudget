from pathlib import Path

import pandas as pd

from exceptions import InvalidStmtFile

__all__ = [
    "load_statement_as_pd"
]


def load_statement_as_pd(filename: Path) -> pd.DataFrame:
    # try each loader
    try:
        from statement_readers.bmo import bmo_credit_csv_loader
        statement_pd = bmo_credit_csv_loader(filename)
        return statement_pd
    except InvalidStmtFile:
        pass

    # not a valid statement file
    raise InvalidStmtFile

    # remove the processed file
    # filename.unlink()
