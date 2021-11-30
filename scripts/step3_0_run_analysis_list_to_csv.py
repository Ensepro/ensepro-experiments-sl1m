import json
import pandas

import pandas as pd

df = pd.read_json("../analyses/base_sl1m/analysis_list.json")
df.to_csv("../analyses/base_sl1m/analysis_list.csv", index=None)

df = pd.read_json("../analyses/all/analysis_list.json")
df.to_csv("../analyses/all/analysis_list.csv", index=None)