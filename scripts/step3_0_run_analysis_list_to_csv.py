import json
import pandas

import pandas as pd

df = pd.read_json("../analyses/analysis_list.json")
df.to_csv("../analyses/analysis_list.csv", index=None)

exit()


def load_json(file):
    return json.loads(open(file=file, mode="r", encoding="utf-8").read())


def save_as_json(value, filename, indent=2, sort_keys=False):
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )


def initialize_if_empty(var, index, default):
    if var and index in var:
        return var[index]
    return default


google_sheets_max_precision = 10
analyses = load_json("analyses/analysis_list.json")
rt = {}
rto = {}
tt = {}
ca = {}
ls1 = {}
ls2 = {}

types = ["slm1", "base"]
slm1_only_l1_options = ["True", "False"]
sizes = ['10', '50', '75', '100', '150', '200', '300', '400', '500', '600', '750', '1000', '2000']

for index1 in analyses:
    for size in analyses[index1]:
        # default_value = {}
        # if size == "frase":
        #     default_value = []

        rt[size] = initialize_if_empty(rt, size, {})
        rto[size] = initialize_if_empty(rto, size, {})
        tt[size] = initialize_if_empty(tt, size, {})
        ca[size] = initialize_if_empty(ca, size, {})
        ls1[size] = initialize_if_empty(ls1, size, {})
        ls2[size] = initialize_if_empty(ls2, size, {})

        if size == "frase":
            continue

        for type in analyses[index1][size]:
            rt[size][type] = initialize_if_empty(rt[size], type, {})
            rto[size][type] = initialize_if_empty(rto[size], type, {})
            tt[size][type] = initialize_if_empty(tt[size], type, {})
            ca[size][type] = initialize_if_empty(ca[size], type, {})
            ls1[size][type] = initialize_if_empty(ls1[size], type, {})
            ls2[size][type] = initialize_if_empty(ls2[size], type, {})

            for slm1_only_l1_option in analyses[index1][size][type]:
                rt[size][type][slm1_only_l1_option] = initialize_if_empty(rt[size][type], slm1_only_l1_option, [])
                rto[size][type][slm1_only_l1_option] = initialize_if_empty(rto[size][type], slm1_only_l1_option, [])
                tt[size][type][slm1_only_l1_option] = initialize_if_empty(tt[size][type], slm1_only_l1_option, [])
                ca[size][type][slm1_only_l1_option] = initialize_if_empty(ca[size][type], slm1_only_l1_option, [])
                ls1[size][type][slm1_only_l1_option] = initialize_if_empty(ls1[size][type], slm1_only_l1_option, [])
                ls2[size][type][slm1_only_l1_option] = initialize_if_empty(ls2[size][type], slm1_only_l1_option, [])

# print(rt)
# exit()
for index in analyses:
    analysis = analyses[index]
    print(analysis)
    # rt["frase"].append(analysis["frase"])
    # rto["frase"].append(analysis["frase"])
    # tt["frase"].append(analysis["frase"])
    # ca["frase"].append(analysis["frase"])
    # ls1["frase"].append(analysis["frase"])
    # ls2["frase"].append(analysis["frase"])

    for type in types:
        for slm1_only_l1_option in slm1_only_l1_options:
            for size in sizes:
                if type is "base":
                    slm1_only_l1_option = 'base'
                    size = 'base'

                ranking_time = round(analysis[size][type][slm1_only_l1_option].get("ranking_time", -1),
                                     google_sheets_max_precision)
                ranking_time_only = round(analysis[size][type][slm1_only_l1_option].get("ranking_time_only", -1),
                                          google_sheets_max_precision)
                total_time = round(analysis[size][type][slm1_only_l1_option].get("total_time", -1),
                                   google_sheets_max_precision)
                has_answer = analysis[size][type][slm1_only_l1_option].get("has_answer", None)
                l1size = analysis[size][type][slm1_only_l1_option].get("l1size", "-1")
                l2size = analysis[size][type][slm1_only_l1_option].get("l2size", "-1")

                rt[size][type][slm1_only_l1_option].append(ranking_time)
                rto[size][type][slm1_only_l1_option].append(ranking_time_only)
                tt[size][type][slm1_only_l1_option].append(total_time)
                ca[size][type][slm1_only_l1_option].append(has_answer)
                ls1[size][type][slm1_only_l1_option].append(l1size)
                ls2[size][type][slm1_only_l1_option].append(l2size)

tables = [
    {"name": "rt", "table": rt},
    {"name": "rto", "table": rto},
    {"name": "tt", "table": tt},
    {"name": "ca", "table": ca},
    {"name": "ls1", "table": ls1},
    {"name": "ls2", "table": ls2},
]

for table in tables:
    table_name = "analyses/table_{table}".format(table=table["name"])
    pandas.DataFrame(table["table"]).to_csv(table_name + ".csv", index=False)
    save_as_json(table["table"], table_name + ".json")
