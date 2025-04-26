"""
Helper functions for model evaluation
"""

from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

TEST_SET_PATH: str = "test_set/"
TEST_SET_DATAFRAME_FILENAME: str = "test_set.csv"
TEST_SET_FILENAMES: list[str] = [
    "1409.0575.pdf",
    "1512.03385.pdf",
    "1603.02754.pdf",
    "1706.03762.pdf",
    "1810.04805.pdf",
    "2209.00939.pdf",
    "2311.01901.pdf",
    "2311.05232.pdf",
    "43022.pdf",
    "Gradient-based_learning_applied_to_document_recognition.pdf",
]


def evaluate_model(
    preds: np.array,
    df_test: pd.DataFrame,
    years_col: str = "year",
    name_col: str = "name",
) -> dict[str, float]:

    # parsing years and names from preds
    years = [int(pred.split("_")[0]) for pred in preds]
    names = [pred.split("_")[1] for pred in preds]

    # making evaluation dictionary for outputting
    eval_dict = {
        "years_accuracy": accuracy_score(years, df_test[years_col].values),
        "names_accuracy": accuracy_score(names, df_test[name_col].values),
    }

    return eval_dict
