import sys
import pandas as pd
import numpy as np

data_path = "housingdata1718.csv"
h_data_raw = pd.read_csv(data_path)
print(h_data_raw)

#h_data_raw["individual"] = h_data_raw["individual"].astype(str).str[0:4].astype(int)
toAmend = ["individual", "group_2", "group_3", "group_4"]
for c in toAmend:
    c_np = np.copy(h_data_raw[c])
    #print(c_np)
    for r in range(h_data_raw.shape[0]):
        val, toSet = c_np[r], ""
        if ("no" in str(val) and "room" in str(val)) or str(val) == "n/a":
            toSet = np.nan
        elif "all" in str(val):
            toSet = 3000
        elif len(str(val)) > 4:
            toSet = int(str(val)[0:4])
        else:
            toSet = val
            #print(val)
        # if str(val)[0] == "0":
        #     toSet = str(val)[1:] if len(str(toSet)) == 0 else int(str(toSet)[1:])

        c_np[r] = toSet
    h_data_raw[c] = c_np
print(h_data_raw)
h_data_raw.to_csv("housingData1718_cleaned.csv")