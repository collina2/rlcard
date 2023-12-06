import sys

sys.path.insert(1, '../')

from rlcard.utils import plot_curve_best_fit

csv_path = "experiments/v1_ep100_g100_ev1_seed42/performance.csv"
fig_path = "experiments/v1_ep100_g100_ev1_seed42/best_line_fig.png"


plot_curve_best_fit(csv_path, fig_path, "nfsp")