import json
import pandas

import pandas as pd

df = pd.read_json("../analyses/analysis_list.json")
df.to_csv("../analyses/analysis_list.csv", index=None)