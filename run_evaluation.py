"""Script for running evaluation of model performance on correctly identifying years and authors of papers."""

import argparse
import os

import pandas as pd
from loguru import logger

from gpt_paper_title import get_paper_file_name
from helpers import evaluate_model


def run_evaluation(
    input_path: str, df_path: str, api_key_path: str
) -> dict[str, float]:
    """
    Estimates ability of model to correctly extract years and names of papers.
    Papers in `input_path` have names generated, which are then compared to the ground truth data in `df_path`.

    Parameters
    ----------
    input_path : str
        Directory of files to include in evaluation. All PDFs in this directory are included in the evaluation.
    df_path : str
        CSV file containing file names, author names, and years, to be compared to LLM-generated names.
    api_key_path : str
        Path to the file where the LLM API key is located.

    Returns
    -------
    dict[str, float]
        Dictionary of metrics, including accuracy on getting the years and author names correct.
    """
    df_test = pd.read_csv(input_path + df_path)

    input_file_names = list(
        filter(lambda x: x.endswith(".pdf"), os.listdir(input_path))
    )

    # generate names of files from papers
    preds = [
        get_paper_file_name(input_path, input_file_name, api_key_path=api_key_path)
        for input_file_name in input_file_names
    ]

    return evaluate_model(preds, df_test)


if __name__ == "__main__":
    logger.info("Running evaluation")

    # Parsing command line arguments
    parser = argparse.ArgumentParser(
        description="Process some arguments.", argument_default=None
    )
    parser.add_argument("--input_path", required=False, default="test_set/")
    parser.add_argument("--df_path", required=False, default="test_set.csv")
    parser.add_argument("--api_key_path", required=True)

    args = parser.parse_args()
    input_path = args.input_path
    df_path = args.df_path
    api_key_path = args.api_key_path

    eval_dict = run_evaluation(
        input_path=input_path,
        df_path=df_path,
        api_key_path=api_key_path,
    )

    logger.info(f"Model evaluation metrics are: {eval_dict}")
