from pathlib import Path
import logging

import pandas as pd
from omegaconf import DictConfig

from exceptions import InvalidStmtFile
from desc_classifier import BaseDescClassifier
from statement_readers import load_statement_as_pd


def process_new_statements(
    statements_folder: Path, 
    all_statements: pd.DataFrame,
    desc_classifier_cfg: DictConfig
) -> pd.DataFrame:
    desc_classifier: BaseDescClassifier = BaseDescClassifier.get_classifier(**desc_classifier_cfg)

    # process statement files from the statements folder
    for file in statements_folder.iterdir():
        try:
            new_statements_pd = load_statement_as_pd(file)
        except InvalidStmtFile as e:
            logging.error(f"Invalid statement file {file}: {e}, skipping.")
            continue
        
        if not set(new_statements_pd.columns).issubset(set(all_statements.columns)):
            logging.error(f"File {file} has different columns, skipping.")
            continue

        if new_statements_pd.index.names != all_statements.index.names:
            logging.error(f"File {file} has different index names, skipping.")
            continue

        # ensure the index is unique
        if not new_statements_pd.index.is_unique:
            logging.error(f"File {file} has non-unique transactions, skipping.")
            continue

        overlap = new_statements_pd.index.isin(all_statements.index)
        if overlap.any():
            logging.warning(f"Removing duplicate transactions from {file}.")
            # remove the overlapping rows
            new_statements_pd = new_statements_pd[~overlap]

        # check if the dataframe is Ok for concatenation
        if new_statements_pd.empty:
            logging.warning(f"Skipping empty file: {file}")
            continue

        if new_statements_pd.isna().any().any():
            logging.error(f"File {file} contains NaN values, skipping.")
            continue

        # the following AI processes are only applied if there are new statements
        all_statements["category"] = all_statements["description"].apply(lambda x: desc_classifier.classify(x))

        all_statements = pd.concat([all_statements, new_statements_pd])

    return all_statements
