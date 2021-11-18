import json
import subprocess
import time
from pathlib import Path
from unicodedata import normalize

base_command = "python3.7 /ensepro-core/main/ensepro_main.py "

isascii = lambda word: len(word) == len(word.encode())


def remover_acentos(text: str):
    return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


def normalize_frase(frase: str):
    return remover_acentos(frase).replace("?", "").replace(",", "").replace(" ", "_")


def execEnsepro(type, file_config, jar, size=0, slm1_only_l1=False):
    # update jar
    configs = json.loads(open(file=file_config, mode="r", encoding="utf-8").read())

    configs["cbc"]["path_answer_generator"] = jar
    configs["cbc"]["slm1_factor"] = size
    configs["cbc"]["slm1_factor_only_l1"] = slm1_only_l1
    size = size if size > 0 else 'base'
    save_as_json(configs, file_config)
    path = "/root/resultados/" + str(type) + "/"
    if size != "base":
        path = path + str(slm1_only_l1) + "/"
    path = path + str(size) + "/"
    Path(path).mkdir(parents=True, exist_ok=True)
    i = 0
    for frase in frases:
        print(type, size, slm1_only_l1, i, "running...")
        filename = "{:0>3d}-slm1-x{size}-".format(i, size=size) + normalize_frase(frase)
        params_command = "-save-json -filename \"{filename}\" -frase \"{frase}\" -resposta"

        final_command = base_command + params_command.format(frase=frase, filename=path + filename)

        timeout_seconds = 300
        timeout = False
        start = time.time_ns()
        try:
            subprocess.check_output(final_command, shell=True, timeout=timeout_seconds)
        except Exception as ignored:
            timeout = True
            pass
        end = time.time_ns()

        try:
            response_file = json.loads(open(file=path + filename + ".json", mode="r", encoding="utf-8").read())

            if not response_file[0]["resposta"]:
                response_file[0]["resposta"] = {}

            # response_file[0]["resposta"]["total_time"] = (end - start) * 1000  # converts to ms
            response_file[0]["resposta"]["total_time"] = (end - start)  # in nanoseconds
            response_file[0]["resposta"]["timeout"] = timeout
            save_as_json(response_file, path + filename + ".json")
        except Exception as e:
            print(e)
        i += 1


def save_as_json(value, filename, indent=2, sort_keys=False):
    import json
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )


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


base_jar = "/jars/ensepro-answer-generator-size-base.jar"
slm1_jar = "/jars/ensepro-answer-generator-size-slm1.jar"
configs_file = "/ensepro-core/ensepro/configuracoes/configs.json"
frases = carregar_frases("../phrases/qald7.txt")
slm1_only_l1_options = [True, False]
sizes = [10, 50, 75, 100, 150, 200, 300, 400, 500, 750, 1000]

for slm1_only_l1 in slm1_only_l1_options:
    for size in sizes:
        execEnsepro("slm1", configs_file, slm1_jar, size, slm1_only_l1)
execEnsepro("base", configs_file, base_jar)

configs_file = "/ensepro-core/ensepro/configuracoes/configs.json"
slm1_only_l1_options = [True, False]
sizes = [10, 50, 75, 100, 150, 200, 300, 400, 500, 750, 1000]

all_jar = "/jars/ensepro-answer-generator-"
jars = [
    "all2",
    "all3",
    "all4",
    "all5"
]

for jar in jars:
    for slm1_only_l1 in slm1_only_l1_options:
        for size in sizes:
            execEnsepro(jar, configs_file, all_jar + jar + ".jar", size, slm1_only_l1)
