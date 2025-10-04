import polars as pl
from env_trading import DiscreteTradingEnv
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

def load_and_split(path: str, split_ratio=0.7):
    df = pl.read_parquet(path)
    # Basic z-score scaling for features (exclude price/volume/return)
    exclude = {"close","high","low","volume","ret1"}
    feat_cols = [c for c in df.columns if c not in exclude]
    df = df.with_columns([ ((pl.col(c) - pl.col(c).mean()) / (pl.col(c).std() + 1e-6)).alias(c) for c in feat_cols ])
    split = int(split_ratio * df.height)
    return df[:split], df[split:], feat_cols

def main():
    train_df, test_df, feat_cols = load_and_split("MSFT_features.parquet")

    env = DummyVecEnv([lambda: DiscreteTradingEnv(train_df, feature_cols=feat_cols, ret_col="ret1",
                                                  trade_cost=0.0005, holding_cost=0.0, window=20)])
    model = DQN("MlpPolicy", env, verbose=1, learning_rate=1e-4,
                buffer_size=100_000, batch_size=256, target_update_interval=1_000)
    model.learn(total_timesteps=200_000)

    # Quick evaluation roll-out
    eval_env = DiscreteTradingEnv(test_df, feature_cols=feat_cols, ret_col="ret1",
                                  trade_cost=0.0005, holding_cost=0.0, window=20)
    obs, _ = eval_env.reset()
    done = False
    eq_curve = []
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, term, trunc, info = eval_env.step(action)
        eq_curve.append(info["equity"])
        done = term or trunc

    print("Final equity (OOS):", eq_curve[-1] if eq_curve else None)

if __name__ == "__main__":
    main()
