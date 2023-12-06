import torch
import sys
sys.path.insert(1, '../')
import rlcard
from rlcard.utils import (
    plot_curve_best_fit,
)

csv_path = "experiments/uno_dqn_result_cr_huge/performance.csv"
fig_path = "experiments/uno_dqn_result_cr_huge/fig_best_fit.png"


# Plot the learning curve
plot_curve_best_fit(csv_path, fig_path, "dqn", degree=1)