



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
    index = type
    index+= 'sl1m' if slm1_only_l1_option else 'sl1mn'
    index+= '-'+str(size)
    for i, frase in enumerate(frases):
        try:
            name = base_path.format(i, frase=normalize_frase(frase), size=size, type=type,
                                    slm1_only_l1_option=slm1_only_l1_option + '/')
            analysis = load_json(name)
        except Exception as e:
            analysis = [{"resposta": {"ranking_time_only": -1, "ranking_time": -1, "total_time": -1}}]
            print("file not found!", e)



        if index not in analysis_map:
            analysis_map[index] = 0


        stats = analysis[0]["resposta"].get("stats", {})
        if stats:
            if stats.get("exception", False):
                analysis_map[index] += 1


analysis_map = {}
base_path = "../resultados2/{type}/{slm1_only_l1_option}{size}/{:0>3d}-slm1-x{size}-{frase}.json"
frases = carregar_frases("../phrases/qald7.txt")
types = ["all2","all3", "all4", "all5"]
slm1_only_l1_options = ["True", "False"]
sizes = ['10', '30', '50', '75', '100', '150', '200', '300', '400', '500', '750']

for type in types:
    for slm1_only_l1_option in slm1_only_l1_options:
        for size in sizes:
            to_list(type, size, slm1_only_l1_option)


filtered = {k: v for k, v in analysis_map.items() if v is not 0}
analysis_map.clear()
analysis_map.update(filtered)
save_as_json(analysis_map, "../analyses/all/timeouts.json")
