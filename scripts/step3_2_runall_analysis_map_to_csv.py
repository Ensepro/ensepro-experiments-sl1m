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
analyses = load_json("../analyses/all/analysis_map.json")
rt = {}
rto = {}
tt = {}
ca = {}
ls1 = {}
ls2 = {}

allxtypes = ['all2', 'all3']
sl1mtypes = ["slm1", "slm1n"]
types = []
for allxtype in allxtypes:
    for sl1mtype in sl1mtypes:
        types.append(allxtype + sl1mtype)

sizes = ['10', '30', '50', '75', '100', '150', '200', '300', '400', '500', '750']
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

    in_order = []
    for size in analyses[question]:
        if size != "frase" and size != "base":
            in_order.append(int(size))

    in_order.sort()
    for size in in_order:
        for type in types:
            print(question, size, type)

            rt_cols.append(analyses[question][str(size)][type].get("ranking_time"))
            rto_cols.append(analyses[question][str(size)][type].get("ranking_time_only"))
            tt_cols.append(analyses[question][str(size)][type].get("total_time"))
            ca_cols.append(analyses[question][str(size)][type].get("has_answer"))
            az_cols.append(analyses[question][str(size)][type].get("answer_size"))
            ls1_cols.append(analyses[question][str(size)][type].get("l1size", -1))
            ls2_cols.append(analyses[question][str(size)][type].get("l2size", -1))
            ls3_cols.append(analyses[question][str(size)][type].get("l3size", -1))
            ls4_cols.append(analyses[question][str(size)][type].get("l4size", -1))
            ls5_cols.append(analyses[question][str(size)][type].get("l5size", -1))
            ls6_cols.append(analyses[question][str(size)][type].get("l6size", -1))

    rt_rows.append(rt_cols)
    rto_rows.append(rto_cols)
    tt_rows.append(tt_cols)
    ca_rows.append(ca_cols)
    az_rows.append(az_cols)
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
        # df.replace(False, 0, inplace=True)
        # df.replace(True, 1, inplace=True)
        df.to_csv("../analyses/all/csv/" + table["name"] + ".csv", sep=";")
    except Exception as n:
        print(table["name"], n)
