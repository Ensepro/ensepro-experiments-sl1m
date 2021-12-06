import json
import pandas


def load_json(file):
    return json.loads(open(file=file, mode="r", encoding="utf-8").read())


def calculate_recall(gold_size, correto_size):
    if correto_size == 0:
        return 0
    return correto_size / gold_size


def calculate_precision(correto_size, respostas_size):
    if respostas_size == 0:
        return 0
    return correto_size / respostas_size


def calculate_f1_score(recall, precision):
    if recall + precision == 0:
        return 0
    return 2 * ((recall * precision) / (recall + precision))


qald7 = load_json("../phrases/analised_qald7_pt.json")
ensepro = load_json("../analyses/base_sl1m/analysis_map.json")
metrics = [
    "GOLD",
    "Correto",
    "#respostas",
    "Recall per question",
    "Precision per question",
    "F1 score per question",
]

allxtypes = []
sl1mtypes = ["slm1", "slm1n"]
types = ["base"]
types = types + sl1mtypes
for allxtype in allxtypes:
    for sl1mtype in sl1mtypes:
        types.append(allxtype + sl1mtype)
sizes = ['10', '30', '50', '75', '100', '150', '200', '300', '400', '500']
headers = []
# headers.append("GOLD")

for type in types:
    if type == "base":
        for metric in metrics:
            headers.append(type + "[" + metric + "]")
        continue
    for size in sizes:
        for metric in metrics:
            headers.append(type + "[" + size + "][" + metric + "]")

# header = pandas.MultiIndex.from_product([types, sizes])
phrases = []
rows = []
# rows.append(headers)
# phrases.append(" ")
print(headers)

for question in qald7:
    columns = []
    question_id = str(question["id"])
    phrases.append(question["question"])

    for type in types:
        base_correto = None
        base_respostas = None
        base_recall = None
        base_precision = None
        base_f1_score = None
        sl1m_correto = None
        sl1m_respostas = None
        sl1m_recall = None
        sl1m_precision = None
        sl1m_f1_score = None

        if type == "base":
            base = ensepro[question_id]["base"]["base"]
            # GOLD number of questions
            GOLD_answer_size = question["answer_size"]

            # ENSEPRO Correto
            base_correto = 0
            if not base["has_answer"]:
                base_correto = 0
            else:
                for triple in base["answers"]:
                    for gold_answer in question["answers"]:
                        if set(triple).issubset(set(gold_answer)):
                            base_correto += 1

            base_correto = GOLD_answer_size if base_correto > GOLD_answer_size else base_correto

            # ENSEPRO #respostas
            base_respostas = 0 if str(base["answer_size"]) == "-1" else base["answer_size"]

            if GOLD_answer_size == 0 and base_respostas == 0 and base_correto == 0:
                GOLD_answer_size = base_respostas = base_correto = 1

            # Recall per question
            base_recall = calculate_recall(GOLD_answer_size, base_correto)

            # Precision per question
            base_precision = calculate_precision(base_correto, base_respostas)

            # F1 score per question
            base_f1_score = calculate_f1_score(base_recall, base_precision)

            columns.append(GOLD_answer_size)
            columns.append(base_correto)
            columns.append(base_respostas)
            columns.append(base_recall)
            columns.append(base_precision)
            columns.append(base_f1_score)

        else:
            for size in sizes:
                sl1m = ensepro[question_id][size][type]

                # GOLD number of questions
                GOLD_answer_size = question["answer_size"]

                # ENSEPRO Correto
                sl1m_correto = 0
                if not sl1m["has_answer"]:
                    sl1m_correto = 0
                else:
                    for triple in sl1m["answers"]:
                        for gold_answer in question["answers"]:
                            if set(triple).issubset(set(gold_answer)):
                                sl1m_correto += 1

                sl1m_correto = GOLD_answer_size if sl1m_correto > GOLD_answer_size else sl1m_correto

                # ENSEPRO #respostas
                sl1m_respostas = 0 if str(sl1m["answer_size"]) == "-1" else sl1m["answer_size"]

                if GOLD_answer_size == 0 and sl1m_respostas == 0 and sl1m_correto == 0:
                    GOLD_answer_size = sl1m_respostas = sl1m_correto = 1

                # Recall per question
                sl1m_recall = calculate_recall(GOLD_answer_size, sl1m_correto)

                # Precision per question
                sl1m_precision = calculate_precision(sl1m_correto, sl1m_respostas)

                # F1 score per question
                sl1m_f1_score = calculate_f1_score(sl1m_recall, sl1m_precision)

                columns.append(GOLD_answer_size)
                columns.append(sl1m_correto)
                columns.append(sl1m_respostas)
                columns.append(sl1m_recall)
                columns.append(sl1m_precision)
                columns.append(sl1m_f1_score)

    rows.append(columns)

for row in rows:
    print(row)
# print(len(rows))
df = pandas.DataFrame(rows, dtype=float, index=phrases, columns=headers)
# s = pandas.to_numeric(df[0])
# print(s)
# print(df.dtypes)
#
df.to_csv("../analyses/base_sl1m/csv/f1_scores.csv", sep=";", decimal=',', float_format='%.8f')
