import json
from unicodedata import normalize

isascii = lambda word: len(word) == len(word.encode())


def remover_acentos(text: str):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def normalize_frase(frase: str):
    return remover_acentos(frase).replace("?", "").replace(",", "").replace(" ", "_")


def load_json(file):
    return json.loads(open(file=file, mode="r", encoding="utf-8").read())


def save_as_json(value, filename, indent=2, sort_keys=False):
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )


def extract_answers(correct_answers):
    answers = []
    for answer in correct_answers:
        for triple in answer["triples"]:
            elements = []
            for element in triple:
                try:

                    new_element = str(element) \
                        .replace("*", "") \
                        # .replace("___", "_") \
                        # .replace("__", "_") \
                        # .replace("(", "") \
                        # .replace(")", "") \
                        # .lower()
                    elements.append(new_element)
                except Exception as e:
                    print(e)
                    raise e
            answers.append(elements)
    return answers


def carregar_frases(arquivo):
    frases = []
    with open(arquivo, mode="r", encoding="UTF-8") as frases_arquivo:
        for frase in frases_arquivo:
            frase = frase.replace("\n", "")
            if not frase:
                continue
            if frase.startswith("#"):
                continue
            frases.append(frase)

    return frases


def to_list(type, size, slm1_only_l1_option):
    for i, frase in enumerate(frases):
        if type is "base":
            slm1_only_l1_option = ''
            size = 'base'
        try:
            name = base_path.format(i, frase=normalize_frase(frase), size=size, type=type,
                                    slm1_only_l1_option=slm1_only_l1_option + '/')
            analysis = load_json(name)
        except Exception as e:
            analysis = [{"resposta": {"ranking_time_only": -1, "ranking_time": -1, "total_time": -1}}]
            print("file not found!", e)

        slm1_only_l1_option = slm1_only_l1_option if slm1_only_l1_option else 'base'
        size = size if size else 'base'

        if i not in analysis_map:
            analysis_map[i] = {}
        if not size in analysis_map[i]:
            analysis_map[i][size] = {}
        if not type in analysis_map[i][size]:
            analysis_map[i][size][type] = {}
        if not slm1_only_l1_option in analysis_map[i][size][type]:
            analysis_map[i][size][type][slm1_only_l1_option] = {}

        analysis_map[i]["frase"] = frase
        analysis_map[i][size][type][slm1_only_l1_option]["ranking_time"] = analysis[0]["resposta"].get(
            "ranking_time", -1)
        analysis_map[i][size][type][slm1_only_l1_option]["ranking_time_only"] = analysis[0]["resposta"].get(
            "ranking_time_only", -1)
        analysis_map[i][size][type][slm1_only_l1_option]["total_time"] = analysis[0]["resposta"]["total_time"]
        analysis_map[i][size][type][slm1_only_l1_option]["timeout"] = analysis[0]["resposta"].get("timeout", "-1")

        correct_answers = analysis[0]["resposta"].get("correct_answer", [])
        has_correct_answer = False

        if correct_answers:
            has_correct_answer = True



        answers = extract_answers(correct_answers)
        analysis_map[i][size][type][slm1_only_l1_option]["answers"] = answers
        analysis_map[i][size][type][slm1_only_l1_option]["has_answer"] = has_correct_answer

        if analysis[0]["resposta"].get("timeout", False):
            answer_size = "-1"
        else:
            answer_size = len(answers)
        analysis_map[i][size][type][slm1_only_l1_option]["answer_size"] = answer_size

        data = {}
        data["id"] = i
        data["size"] = size
        data["type"] = type
        data["slm1_only_l1_option"] = slm1_only_l1_option
        data["ranking_time"] = analysis[0]["resposta"].get("ranking_time", -1)
        data["ranking_time_only"] = analysis[0]["resposta"].get("ranking_time_only", -1)
        data["total_time"] = analysis[0]["resposta"].get("total_time", -1)
        data["has_answer"] = has_correct_answer
        data["answer_size"] = answer_size
        data["timeout"] = analysis[0]["resposta"].get("timeout", "-1")

        lsizes = analysis[0]["resposta"].get("l_sizes", [])
        for index, lsize in enumerate(lsizes):
            data["l" + str(index + 1) + "size"] = lsize
            analysis_map[i][size][type][slm1_only_l1_option]["l" + str(index + 1) + "size"] = lsize

        analysis_list.append(data)


base_path = "../resultados2/{type}/{slm1_only_l1_option}{size}/{:0>3d}-slm1-x{size}-{frase}.json"
frases = carregar_frases("../phrases/qald7.txt")

analysis_map = {}
analysis_list = []
types = ["slm1"]
slm1_only_l1_options = ["True", "False"]
sizes = ['10', '30', '50', '75', '100', '150', '200', '300', '400', '500']

for type in types:
    for slm1_only_l1_option in slm1_only_l1_options:
        for size in sizes:
            to_list(type, size, slm1_only_l1_option)

to_list("base", "base", "base")

analysis_list.sort(key=lambda x: x["id"])
save_as_json(analysis_map, "../analyses/base_sl1m/analysis_map_pre.json")
save_as_json(analysis_list, "../analyses/base_sl1m/analysis_list.json")

print("##################################################################################")
analysis_map = {}
analysis_list = []
types = ["all2", "all3"]
slm1_only_l1_options = ["True", "False"]
sizes = ['10', '30', '50', '75', '100', '150', '200', '300', '400', '500', '750']

for type in types:
    for slm1_only_l1_option in slm1_only_l1_options:
        for size in sizes:
            to_list(type, size, slm1_only_l1_option)

analysis_list.sort(key=lambda x: x["id"])
save_as_json(analysis_map, "../analyses/all/analysis_map_pre.json")
save_as_json(analysis_list, "../analyses/all/analysis_list.json")