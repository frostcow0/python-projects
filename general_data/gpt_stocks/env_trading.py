
import numpy as np
import polars as pl
import gymnasium as gym
from gymnasium import spaces

class DiscreteTradingEnv(gym.Env):
    """
    Observation: feature vector (optionally stacked with history window)
    Actions: 0=short (-1), 1=flat (0), 2=long (+1)
    Reward_t = position_{t-1} * ret1_t - trade_cost*1{pos changes} - holding_cost*|position_t|
    """
    metadata = {"render_modes": []}

    def __init__(self, feats_df: pl.DataFrame, feature_cols, ret_col="ret1",
                 trade_cost=0.0005, holding_cost=0.0, window:int|None=None):
        super().__init__()
        self.df = feats_df
        self.feature_cols = list(feature_cols)
        self.ret_col = ret_col
        self.trade_cost = float(trade_cost)
        self.holding_cost = float(holding_cost)
        self.window = window

        obs_dim = len(self.feature_cols) * (window if window else 1)
        self.action_space = spaces.Discrete(3)  # 0 short, 1 flat, 2 long
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32)

        self._reset_state()

    def _reset_state(self):
        self.t = 0
        self.position = 0  # -1,0,1
        self.prev_position = 0
        self.equity = 1.0
        self.episode_done = False

        # Pre-extract features matrix for speed
        self.X = self.df.select(self.feature_cols).to_numpy()
        self.rets = self.df[self.ret_col].to_numpy()

    def _get_obs(self):
        if self.window:
            start = max(0, self.t - self.window + 1)
            arr = self.X[start:self.t+1]
            if arr.shape[0] < self.window:
                pad_rows = self.window - arr.shape[0]
                pad = np.repeat(self.X[start:start+1], pad_rows, axis=0)
                arr = np.vstack([pad, arr])
            return arr.reshape(-1).astype(np.float32)
        else:
            return self.X[self.t].astype(np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._reset_state()
        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        if self.episode_done:
            raise RuntimeError("Step called on terminated episode. Call reset().")

        self.prev_position = self.position
        self.position = [-1, 0, 1][int(action)]

        ret = float(self.rets[self.t])
        trade_penalty = self.trade_cost if self.position != self.prev_position else 0.0
        hold_penalty = self.holding_cost * abs(self.position)

        reward = self.prev_position * ret - trade_penalty - hold_penalty
        self.equity *= (1.0 + self.prev_position * ret)

        self.t += 1
        terminated = (self.t >= len(self.rets) - 1)
        truncated = False
        self.episode_done = terminated or truncated

        obs = self._get_obs()
        info = {"equity": self.equity, "position": self.position, "ret": ret, "t": self.t}
        return obs, reward, terminated, truncated, info


class ContinuousTradingEnv(gym.Env):
    """
    Continuous position sizing environment.

    Action space: Box([-1, 1]) -> target net position (short to long).
    Reward_t = pos_{t-1} * ret1_t - trade_cost * |pos_t - pos_{t-1}| - holding_cost * |pos_t|
    Equity is compounded by (1 + pos_{t-1} * ret1_t).

    Args:
        feats_df: Polars DataFrame with features and a return column.
        feature_cols: list of feature column names.
        ret_col: string name of return column (e.g., 'ret1').
        trade_cost: cost per unit position change (e.g., 0.0005 = 5 bps) per step.
        holding_cost: per-step cost per unit absolute position.
        window: optional history length to stack into observations.
        max_leverage: clip absolute position to this cap (>=1.0).
        action_smoothing: float in [0,1]; pos_t = (1-a)*pos_{t-1} + a*action_t.
    """
    metadata = {"render_modes": []}

    def __init__(self, feats_df: pl.DataFrame, feature_cols, ret_col="ret1",
                 trade_cost=0.0005, holding_cost=0.0, window:int|None=None,
                 max_leverage: float = 1.0, action_smoothing: float = 1.0):
        super().__init__()
        self.df = feats_df
        self.feature_cols = list(feature_cols)
        self.ret_col = ret_col
        self.trade_cost = float(trade_cost)
        self.holding_cost = float(holding_cost)
        self.window = window
        self.max_leverage = float(max_leverage)
        self.smooth = float(action_smoothing)

        obs_dim = len(self.feature_cols) * (window if window else 1)
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32)

        self._reset_state()

    def _reset_state(self):
        self.t = 0
        self.position = 0.0
        self.prev_position = 0.0
        self.equity = 1.0
        self.episode_done = False

        self.X = self.df.select(self.feature_cols).to_numpy()
        self.rets = self.df[self.ret_col].to_numpy()

    def _get_obs(self):
        if self.window:
            start = max(0, self.t - self.window + 1)
            arr = self.X[start:self.t+1]
            if arr.shape[0] < self.window:
                pad_rows = self.window - arr.shape[0]
                pad = np.repeat(self.X[start:start+1], pad_rows, axis=0)
                arr = np.vstack([pad, arr])
            return arr.reshape(-1).astype(np.float32)
        else:
            return self.X[self.t].astype(np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._reset_state()
        obs = self._get_obs()
        return obs, {}

    def step(self, action):
        if self.episode_done:
            raise RuntimeError("Step called on terminated episode. Call reset().")

        # ensure proper type/shape
        a = float(np.clip(action[0], -1.0, 1.0))
        self.prev_position = float(self.position)

        # Smooth and cap leverage
        target = a
        self.position = (1.0 - self.smooth) * self.prev_position + self.smooth * target
        self.position = float(np.clip(self.position, -self.max_leverage, self.max_leverage))

        ret = float(self.rets[self.t])
        trade_penalty = self.trade_cost * abs(self.position - self.prev_position)
        hold_penalty = self.holding_cost * abs(self.position)

        reward = self.prev_position * ret - trade_penalty - hold_penalty
        self.equity *= (1.0 + self.prev_position * ret)

        self.t += 1
        terminated = (self.t >= len(self.rets) - 1)
        truncated = False
        self.episode_done = terminated or truncated

        obs = self._get_obs()
        info = {"equity": self.equity, "position": self.position, "ret": ret, "t": self.t}
        return obs, reward, terminated, truncated, info
