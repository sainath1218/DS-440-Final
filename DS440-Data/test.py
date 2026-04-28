import pandas as pd
from collections import Counter
import math
import statistics as stats
import numpy as np

def transform_playfield(x):
  playfield = ["N"] * 400
  
  for i in range(len(x)):
    playfield[i] = x[i]
  
  return "".join(playfield)


def get_cases(df: pd.DataFrame):
  d = df.copy()
  d.columns = d.columns.str.strip()

  # row position in the ORIGINAL df
  d["_pos"] = np.arange(len(d), dtype=int)

  # only use cleared==0 rows to pick the "current" example per (r, placed)
  mask = (d["cleared"] == 0) & (d["immediate_garbage"] == 0)
  d0 = d[mask].copy()

  # first occurrence (by original position) per (r, placed) among cleared==0 rows
  first_pos = (
    d0.groupby(["r", "placed"], sort=False)["_pos"]
      .min()
      .reset_index()
      .rename(columns={"_pos": "pos"})
  )

  # drop cases where the next original row doesn't exist
  first_pos = first_pos[first_pos["pos"] < len(d) - 1].copy()

  cur = d.iloc[first_pos["pos"].to_numpy()]
  nxt = d.iloc[(first_pos["pos"] + 1).to_numpy()]  # next row in ORIGINAL df

  out = pd.DataFrame({
    "r": first_pos["r"].to_numpy(),
    "placed": first_pos["placed"].to_numpy(),
    "x": cur["x"].to_numpy(),
    "y": cur["y"].to_numpy(),
    "playfield": cur["playfield_transformed"].to_numpy(),
    "next_playfield": nxt["playfield_transformed"].to_numpy(),
    "next_cleared": nxt["cleared"].to_numpy(),  # optional, useful for debugging
  })

  out.to_csv("cases.csv", index=False)
  out.to_json("cases.json", index=False)


if __name__=="__main__":
  # df = pd.read_csv("data_transformed.csv")
  # get_cases(df)


  # print(df[df["placed"] == "O"]["r"].unique())
  # df = pd.read_csv("data_transformed.csv")
  # df["playfield_transformed"] = df["playfield"].map(transform_playfield)
  # df.to_csv("data_transformed.csv", index=False)
  # first_per_combo_cleared(df).to_csv("cases.csv", index=False)
  # sample_df = pd.read_csv("sample.csv")
  # sample_df["playfield_transformed"] = sample_df["playfield"].map(transform_playfield)
  # sample_df.to_csv("test_playfield_transformed.csv", index=False)
  # print(f"r values: {df["r"].unique()}")
  # print(f"placed values: {df["placed"].unique()}")
  # cases = collect_28_cases(df, piece_col="playfield")
  # print(cases.head())
  # cases.to_csv("cases.csv")
  # pd.read_csv("cases.csv").to_json("cases.json", index=False)


