import json
import pandas


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
analyses = load_json("../analyses/analysis_map.json")
rt = {}
rto = {}
tt = {}
ca = {}
ls1 = {}
ls2 = {}

types = ["base", "slm1", "slm1n"]
sizes = ['10', '50']  # , '75', '100', '150', '200', '300', '400', '500', '600', '750', '1000']
header = pandas.MultiIndex.from_product([types, sizes])

phrases = []
rt_rows = []
rto_rows = []
tt_rows = []
ca_rows = []
az_rows = []
ls1_rows = []
ls2_rows = []
ls3_rows = []
ls4_rows = []
ls5_rows = []
ls6_rows = []

for question in analyses:

    rt_cols = []
    rto_cols = []
    tt_cols = []
    ca_cols = []
    az_cols = []
    ls1_cols = []
    ls2_cols = []
    ls3_cols = []
    ls4_cols = []
    ls5_cols = []
    ls6_cols = []

    phrases.append(analyses[question]["frase"])

    rt_cols.append(analyses[question]["base"]["base"].get("ranking_time"))
    rto_cols.append(analyses[question]["base"]["base"].get("ranking_time_only"))
    tt_cols.append(analyses[question]["base"]["base"].get("total_time"))
    ca_cols.append(analyses[question]["base"]["base"].get("has_answer"))
    az_cols.append(analyses[question]["base"]["base"].get("answer_size"))
    ls1_cols.append(analyses[question]["base"]["base"].get("l1size", -1))
    ls2_cols.append(analyses[question]["base"]["base"].get("l2size", -1))
    ls3_cols.append(analyses[question]["base"]["base"].get("l3size", -1))
    ls4_cols.append(analyses[question]["base"]["base"].get("l4size", -1))
    ls5_cols.append(analyses[question]["base"]["base"].get("l5size", -1))
    ls6_cols.append(analyses[question]["base"]["base"].get("l6size", -1))
    for _s in sizes[:-1]:
        rt_cols.append("remove column")
        rto_cols.append("remove column")
        tt_cols.append("remove column")
        ca_cols.append("remove column")
        az_cols.append("remove column")
        ls1_cols.append("remove column")
        ls2_cols.append("remove column")
        ls3_cols.append("remove column")
        ls4_cols.append("remove column")
        ls5_cols.append("remove column")
        ls6_cols.append("remove column")
    in_order = []
    for type in analyses[question]:
        if type != "frase" and type != "base":
            in_order.append(int(type))

    in_order.sort()
    for type in in_order:
        for subtype in analyses[question][str(type)]:
            rt_cols.append(analyses[question][str(type)][subtype].get("ranking_time"))
            rto_cols.append(analyses[question][str(type)][subtype].get("ranking_time_only"))
            tt_cols.append(analyses[question][str(type)][subtype].get("total_time"))
            ca_cols.append(analyses[question][str(type)][subtype].get("has_answer"))
            az_cols.append(analyses[question][str(type)][subtype].get("answer_size"))
            ls1_cols.append(analyses[question][str(type)][subtype].get("l1size", -1))
            ls2_cols.append(analyses[question][str(type)][subtype].get("l2size", -1))
            ls3_cols.append(analyses[question][str(type)][subtype].get("l3size", -1))
            ls4_cols.append(analyses[question][str(type)][subtype].get("l4size", -1))
            ls5_cols.append(analyses[question][str(type)][subtype].get("l5size", -1))
            ls6_cols.append(analyses[question][str(type)][subtype].get("l6size", -1))

    rt_rows.append(rt_cols)
    rto_rows.append(rto_cols)
    tt_rows.append(tt_cols)
    ca_rows.append(ca_cols)
    az_rows.append(ca_cols)
    ls1_rows.append(ls1_cols)
    ls2_rows.append(ls2_cols)
    ls3_rows.append(ls3_cols)
    ls4_rows.append(ls4_cols)
    ls5_rows.append(ls5_cols)
    ls6_rows.append(ls6_cols)

tables = [
    {
        "name": "rt_rows",
        "table": rt_rows,
    },
    {
        "name": "rto_rows",
        "table": rto_rows,
    },
    {
        "name": "tt_rows",
        "table": tt_rows,
    },
    {
        "name": "ca_rows",
        "table": ca_rows,
    },
    {
        "name": "az_rows",
        "table": az_rows,
    },
    {
        "name": "ls1_rows",
        "table": ls1_rows,
    },
    {
        "name": "ls2_rows",
        "table": ls2_rows,
    },
    {
        "name": "ls3_rows",
        "table": ls3_rows,
    },
    {
        "name": "ls4_rows",
        "table": ls4_rows,
    },
    {
        "name": "ls5_rows",
        "table": ls5_rows,
    },
    {
        "name": "ls6_rows",
        "table": ls6_rows,
    },
]

save_as_json(tables, "temp.json")
for table in tables:
    try:
        df = pandas.DataFrame(table["table"], index=phrases, columns=header)
        # df = pd.DataFrame(table["table"],
        # index=['a','b','c','d','e','f','g'],
        # columns=header)
        df.replace(False, 0, inplace=True)
        df.replace(True, 1, inplace=True)
        df.to_csv("../analyses/csv/" + table["name"] + ".csv")
    except Exception as n:
        print(table["name"], n)

# for type in types:
#     for size in sizes:
#         analyses


exit()
"""



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

            # for slm1_only_l1_option in analyses[index1][size][type]:
            #     rt[size][type][slm1_only_l1_option] = initialize_if_empty(rt[size][type], slm1_only_l1_option, [])
            #     rto[size][type][slm1_only_l1_option] = initialize_if_empty(rto[size][type], slm1_only_l1_option, [])
            #     tt[size][type][slm1_only_l1_option] = initialize_if_empty(tt[size][type], slm1_only_l1_option, [])
            #     ca[size][type][slm1_only_l1_option] = initialize_if_empty(ca[size][type], slm1_only_l1_option, [])
            #     ls1[size][type][slm1_only_l1_option] = initialize_if_empty(ls1[size][type], slm1_only_l1_option, [])
            #     ls2[size][type][slm1_only_l1_option] = initialize_if_empty(ls2[size][type], slm1_only_l1_option, [])

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
        # for slm1_only_l1_option in slm1_only_l1_options:
        for size in sizes:
            if type is "base":
                slm1_only_l1_option = 'base'
                size = 'base'

            ranking_time = round(analysis[size][type].get("ranking_time", -1),
                                 google_sheets_max_precision)
            ranking_time_only = round(analysis[size][type].get("ranking_time_only", -1),
                                      google_sheets_max_precision)
            total_time = round(analysis[size][type].get("total_time", -1),
                               google_sheets_max_precision)
            has_answer = analysis[size][type].get("has_answer", None)
            l1size = analysis[size][type][slm1_only_l1_option].get("l1size", "-1")
            l2size = analysis[size][type][slm1_only_l1_option].get("l2size", "-1")

            rt[size][type][slm1_only_l1_option].append(ranking_time)
            rto[size][type][slm1_only_l1_option].append(ranking_time_only)
            tt[size][type][slm1_only_l1_option].append(total_time)
            ca[size][type][slm1_only_l1_option].append(has_answer)
            ls1[size][type][slm1_only_l1_option].append(l1size)
            ls2[size][type][slm1_only_l1_option].append(l2size)

print()

tables = [
    {"name": "rt", "table": rt},
    {"name": "rto", "table": rto},
    {"name": "tt", "table": tt},
    {"name": "ca", "table": ca},
    {"name": "ls1", "table": ls1},
    {"name": "ls2", "table": ls2},
]

for table in tables:
    lines = []
    for data in table["table"]:
        print(data)
        columns = []

        pass

    continue
    table_name = "../analyses/table_{table}".format(table=table["name"])
    pandas.DataFrame(table["table"], columns=header).to_csv(table_name + ".csv", index=False)
    save_as_json(table["table"], table_name + ".json")
"""
