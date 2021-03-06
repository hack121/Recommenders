# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import pytest
import papermill as pm
from tests.notebooks_common import OUTPUT_NOTEBOOK, KERNEL_NAME


TOL = 0.05


@pytest.mark.integration
@pytest.mark.parametrize(
    "size, result_list",
    [
        ("1m", [0.89, 0.70, 0.36, 0.36, 0.011, 0.10, 0.093, 0.025]),
        # ("10m", [0.56, 0.43, 0.72, 0.72]),  # works but pretty long
    ],
)
def test_surprise_svd_integration(notebooks, size, result_list):
    notebook_path = notebooks["surprise_svd_deep_dive"]
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(MOVIELENS_DATA_SIZE=size),
    )
    nb = pm.read_notebook(OUTPUT_NOTEBOOK)
    df = nb.dataframe
    result_rmse = df.loc[df["name"] == "rmse", "value"].values[0]
    assert result_rmse == pytest.approx(result_list[0], TOL)
    result_mae = df.loc[df["name"] == "mae", "value"].values[0]
    assert result_mae == pytest.approx(result_list[1], TOL)
    result_rsquared = df.loc[df["name"] == "rsquared", "value"].values[0]
    assert result_rsquared == pytest.approx(result_list[2], TOL)
    result_exp_var = df.loc[df["name"] == "exp_var", "value"].values[0]
    assert result_exp_var == pytest.approx(result_list[3], TOL)
    result_MAP = df.loc[df["name"] == "MAP", "value"].values[0]
    assert result_MAP == pytest.approx(result_list[4], TOL)
    result_NDCG = df.loc[df["name"] == "NDCG", "value"].values[0]
    assert result_NDCG == pytest.approx(result_list[5], TOL)
    result_precision = df.loc[df["name"] == "precision", "value"].values[0]
    assert result_precision == pytest.approx(result_list[6], TOL)
    result_recall = df.loc[df["name"] == "recall", "value"].values[0]
    assert result_recall == pytest.approx(result_list[7], TOL)
