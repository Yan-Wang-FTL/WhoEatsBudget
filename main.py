import logging
from pathlib import Path


import pandas as pd
import hydra
from omegaconf import DictConfig

from utils import process_new_statements


@hydra.main(config_path="config", config_name="config.yaml", version_base=None)
def main(cfg: DictConfig):
    # try to load the saved statements
    all_statements_df = pd.DataFrame(columns=["card_num", "transaction_date", "item_num", "posting_date", "amount", "description"])
    all_statements_df.set_index(["card_num", "transaction_date", "item_num"], inplace=True)
    saved_statements_filename = Path(cfg.saved_statements_filename)
    if saved_statements_filename.exists():
        try:
            all_statements_df = pd.read_feather(saved_statements_filename)
            logging.info(f"Loaded saved statements from {saved_statements_filename}")
        except Exception as e:
            logging.error(f"Error loading saved statements: {e}")

    all_statements_df = process_new_statements(Path(cfg.new_statements_folder), all_statements_df, cfg.desc_classifier)

    all_statements_df.to_feather(saved_statements_filename)
    logging.info(f"Saved all statements to {saved_statements_filename}")


if __name__ == "__main__":
    main()