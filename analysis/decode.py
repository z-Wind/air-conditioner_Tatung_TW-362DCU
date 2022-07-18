import pandas as pd

def reverse_code(x):
    x = int(x, 16)
    x = int(f"{x:b}"[::-1], 2)
    return x

df = pd.read_csv("code.csv")
df["irplus編碼"] = df["Arduino編碼"].apply(lambda x: f"0x{reverse_code(x):X}")
df["irplus編碼(二進制)"] = df["Arduino編碼"].apply(lambda x: f"{reverse_code(x):030b}")
df.to_csv("decode.csv")