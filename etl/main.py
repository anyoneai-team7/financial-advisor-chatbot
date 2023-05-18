import logging
import os
import multiprocessing
from src.extract import Extractor
from src.load import Indexer

logging.basicConfig(level=logging.INFO, format="%(processName)s %(message)s")


if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()
    extractor = Extractor(
        parent_conn,
        "anyoneai-datasets",
        "nasdaq_annual_reports",
        os.path.join(os.getcwd(), "dataset"),
    )
    indexer = Indexer(child_conn)

    extractor.start()
    indexer.start()
