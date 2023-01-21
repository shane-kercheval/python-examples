from typing import Callable, Optional
import numpy as np

import arviz as az
import matplotlib.pyplot as plt

from helpsk.string import format_number


def plotly_title(title: str, subtitle: Optional[str] = None) -> str:
    """Formats title and subtitle for plotly graphs."""
    if subtitle:
        return f'{title}<br><sup>{subtitle}</sup>'
    else:
        return title


def plot_hdi(
        samples,
        title: Optional[str] = None,
        transformation: Optional[Callable] = None,
        vertical_factor_66: int = 1,
        vertical_factor_95: int = 1,
        ticks: Optional[list] = None,
        decimals: int = 1):
    """
    Plot the 66% and 95% Hight Density Interval of `samples` passed in. The min, median, and max
    is also plotted.

    Args:
        samples:
            np.array of integers or floats
        title:
            title of the plot
        transformation:
            transformation to do for displaying the min, median, max, and 66% and 95% low and high
            values for the HDI.
    """
    sim_min, sim_median, sim_max = np.quantile(samples, q=[0, 0.5, 1])
    sim_95_hdi_prob_low, sim_95_hdi_prob_hi = az.hdi(samples, hdi_prob=0.95)
    sim_66_hdi_prob_low, sim_66_hdi_prob_hi = az.hdi(samples, hdi_prob=0.66)

    def plot_text(x, label, above=True, factor=1):
        y = 0.018 + (0.025 * (factor - 1))
        if not above:
            y *= -1

        if transformation:
            x_formatted = format_number(transformation(x), places=decimals)
        else:
            x_formatted = format_number(x, places=decimals)

        return plt.text(
            x=x, y=y,
            s=f"{label}:\n{x_formatted}",
            ha='center', va='center', fontsize=9,
        )

    fig, ax = plt.subplots(1)
    plt.plot([sim_min, sim_max], [0, 0], color='gray')
    plt.plot([sim_95_hdi_prob_low, sim_95_hdi_prob_hi], [0, 0], color='black', linewidth=3)
    plt.plot([sim_66_hdi_prob_low, sim_66_hdi_prob_hi], [0, 0], color='black', linewidth=7)
    plt.plot(sim_median, 0, 'o', markersize=15, color='black')
    ax.set_yticklabels([])

    plot_text(x=sim_min, label='min')
    plot_text(x=sim_max, label="max")
    plot_text(x=sim_median, label="median", above=False)
    plot_text(x=sim_66_hdi_prob_low, label="HDI 66", factor=vertical_factor_66)
    plot_text(x=sim_66_hdi_prob_hi, label="HDI 66", factor=vertical_factor_66)
    plot_text(x=sim_95_hdi_prob_low, label="HDI 95", above=False, factor=vertical_factor_95)
    plot_text(x=sim_95_hdi_prob_hi, label="HDI 95", above=False, factor=vertical_factor_95)

    if ticks:
        plt.xticks(ticks)

    if transformation:
        labels = [item.get_text() for item in ax.get_xticklabels()]
        for index in range(len(labels)):
            labels[index] = format_number(
                transformation(float(labels[index].replace('−', '-'))),
                places=decimals
            )
        ax.set_xticklabels(labels)

    fig.set_size_inches(w=7, h=2.2)
    # plt.xlim((115, 195))
    if not title:
        title = "HDI"
    plt.suptitle(title)


def px_log_10_axis(fig, axis='x', min_value=-10, max_value=20, step=1):
    """
    Use this function to transform the ticks/labels of the x-axis of a plotly-express graph to
    log10.

    Example:

    ```
    fig = px.histogram(
        np.log10(values),
        title="Histogram of 'values' (Log10)"
    )
    px_log_10_x_axis(fig)
    ```
    """
    values = list(range(min_value, max_value, step))
    axis_value = dict(
        tickvals=values,
        ticktext=[10 ** x for x in values],
    )
    if axis == 'x':
        fig.update_layout(xaxis=axis_value)
    else:
        fig.update_layout(yaxis=axis_value)
    return fig
