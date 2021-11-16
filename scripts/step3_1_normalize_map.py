import json


def load_json(file):
    return json.loads(open(file=file, mode="r", encoding="utf-8").read())


def save_as_json(value, filename, indent=2, sort_keys=False):
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )


analyses = load_json("../analyses/analysis_map_pre.json")
analyses_pos = {}

for question in analyses:
    if question not in analyses_pos:
        analyses_pos[question] = {}

    for size in analyses[question]:
        if size not in analyses_pos[question]:
            analyses_pos[question][size] = {}
        # print(size)
        if size == "frase":
            analyses_pos[question][size] = analyses[question][size]
            continue

        for type in analyses[question][size]:
            if type not in analyses[question][size]:
                analyses_pos[question][size][type] = {}

            if type == "base":
                analyses_pos[question][size] = analyses[question][size][type]
                continue

            for slm1_only in analyses[question][size][type]:

                newType = "slm1n"
                if slm1_only == "True":
                    newType = "slm1"

                if newType not in analyses[question][size]:
                    analyses_pos[question][size][newType] = {}

                try:
                    analyses_pos[question][size][newType] = analyses[question][size][type][slm1_only]
                except:
                    print("aq")


save_as_json(analyses_pos, "../analyses/analysis_map.json")


