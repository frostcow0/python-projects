
import polars as pl
from env_trading import ContinuousTradingEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from eval_utils import save_equity_csv, make_report_pdf, compute_metrics
from pathlib import Path
import numpy as np

def load_and_split(path: str, split_ratio=0.7):
    df = pl.read_parquet(path)
    exclude = {"close","high","low","volume","ret1"}
    feat_cols = [c for c in df.columns if c not in exclude]
    # Z-score features
    df = df.with_columns([ ((pl.col(c) - pl.col(c).mean()) / (pl.col(c).std() + 1e-6)).alias(c) for c in feat_cols ])
    split = int(split_ratio * df.height)
    return df[:split], df[split:], feat_cols

def roll_out(env):
    obs, _ = env.reset()
    done = False
    equities = [env.equity]
    positions = [env.position]
    while not done:
        # random policy placeholder; replace in evaluation with trained model.predict
        action = np.array([0.0], dtype=np.float32)
        obs, reward, term, trunc, info = env.step(action)
        equities.append(info["equity"])
        positions.append(info["position"])
        done = term or trunc
    return np.array(equities), np.array(positions)

def evaluate_model(model, env):
    obs, _ = env.reset()
    done = False
    equities = [env.equity]
    positions = [env.position]
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, term, trunc, info = env.step(action)
        equities.append(info["equity"])
        positions.append(info["position"])
        done = term or trunc
    return np.array(equities), np.array(positions)

def main():
    feats_path = Path("MSFT_features.parquet")
    outdir = Path("reports"); outdir.mkdir(exist_ok=True)
    train_df, test_df, feat_cols = load_and_split(feats_path.as_posix())

    # Train
    env = DummyVecEnv([lambda: ContinuousTradingEnv(train_df, feature_cols=feat_cols, ret_col="ret1",
                                                    trade_cost=0.0005, holding_cost=0.0, window=20,
                                                    max_leverage=1.0, action_smoothing=0.5)])
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=3e-4, batch_size=4096, n_epochs=10, gae_lambda=0.95, gamma=0.99, clip_range=0.2)
    model.learn(total_timesteps=500_000)

    # Evaluate OOS
    eval_env = ContinuousTradingEnv(test_df, feature_cols=feat_cols, ret_col="ret1",
                                    trade_cost=0.0005, holding_cost=0.0, window=20,
                                    max_leverage=1.0, action_smoothing=0.5)
    equity, positions = evaluate_model(model, eval_env)

    # Save CSV + PDF
    csv_path = outdir / "msft_ppo_equity.csv"
    pdf_path = outdir / "msft_ppo_report.pdf"
    save_equity_csv(equity, csv_path.as_posix())
    metrics = make_report_pdf(equity, positions, pdf_path.as_posix(),
                              title="MSFT PPO (Continuous Position Sizing) Report", periods_per_year=252)

    print("Saved:", csv_path.as_posix(), pdf_path.as_posix())
    print("Metrics:", metrics)

if __name__ == "__main__":
    main()
