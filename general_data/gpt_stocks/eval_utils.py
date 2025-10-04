
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from dataclasses import dataclass

EPS = 1e-12

@dataclass
class PerfMetrics:
    cagr: float
    sharpe: float
    max_drawdown: float
    calmar: float
    volatility: float
    total_return: float

def compute_metrics(equity: np.ndarray, periods_per_year: int = 252) -> PerfMetrics:
    equity = np.asarray(equity, dtype=float)
    if len(equity) < 2:
        return PerfMetrics(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    rets = np.diff(equity) / (equity[:-1] + EPS)
    mean = np.mean(rets)
    std = np.std(rets) + EPS
    sharpe = (mean * np.sqrt(periods_per_year)) / std

    # CAGR
    total_return = (equity[-1] / (equity[0] + EPS)) - 1.0
    years = max(len(rets) / periods_per_year, EPS)
    cagr = (equity[-1] / (equity[0] + EPS)) ** (1.0 / years) - 1.0

    # Max drawdown
    peak = np.maximum.accumulate(equity)
    drawdown = 1.0 - equity / (peak + EPS)
    max_dd = float(np.max(drawdown))

    calmar = cagr / (max_dd + EPS)

    return PerfMetrics(cagr=cagr, sharpe=sharpe, max_drawdown=max_dd,
                       calmar=calmar, volatility=std*np.sqrt(periods_per_year),
                       total_return=total_return)

def save_equity_csv(equity: np.ndarray, path: str):
    df = pd.DataFrame({
        "step": np.arange(len(equity)),
        "equity": equity
    })
    df.to_csv(path, index=False)

def make_report_pdf(equity: np.ndarray, positions: np.ndarray | None, save_path: str, title: str, periods_per_year: int = 252):
    metrics = compute_metrics(equity, periods_per_year=periods_per_year)
    rets = np.diff(equity) / (equity[:-1] + EPS)
    drawdown = 1.0 - equity / (np.maximum.accumulate(equity) + EPS)

    with PdfPages(save_path) as pdf:
        # Page 1: Title + Table
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle(title, fontsize=16)
        ax = fig.add_subplot(2,1,1)
        ax.plot(equity)
        ax.set_title("Equity Curve")
        ax.set_xlabel("Step")
        ax.set_ylabel("Equity")

        ax2 = fig.add_subplot(2,1,2)
        ax2.plot(drawdown)
        ax2.set_title("Underwater (Drawdown)")
        ax2.set_xlabel("Step")
        ax2.set_ylabel("Drawdown")

        pdf.savefig(fig)
        plt.close(fig)

        # Page 2: Metrics table and histogram of returns
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle("Performance Summary", fontsize=16)
        ax = fig.add_subplot(2,1,1)
        # Build a simple table
        table_data = [
            ["Total Return", f"{metrics.total_return:.2%}"],
            ["CAGR", f"{metrics.cagr:.2%}"],
            ["Sharpe", f"{metrics.sharpe:.2f}"],
            ["Volatility (ann.)", f"{metrics.volatility:.2%}"],
            ["Max Drawdown", f"{metrics.max_drawdown:.2%}"],
            ["Calmar", f"{metrics.calmar:.2f}"],
        ]
        ax.axis('off')
        table = ax.table(cellText=table_data, colLabels=["Metric", "Value"], loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        ax2 = fig.add_subplot(2,1,2)
        if len(rets) > 0:
            ax2.hist(rets, bins=50)
        ax2.set_title("Distribution of Returns (per step)")
        ax2.set_xlabel("Return")
        ax2.set_ylabel("Frequency")

        pdf.savefig(fig)
        plt.close(fig)

        # Page 3: Positions (optional)
        if positions is not None and len(positions) == len(equity):
            fig = plt.figure(figsize=(8.5, 4))
            plt.plot(positions)
            plt.title("Position Over Time")
            plt.xlabel("Step")
            plt.ylabel("Net Exposure")
            pdf.savefig(fig)
            plt.close(fig)

    return metrics
