import json


def save_as_json(value, filename, indent=2, sort_keys=False):
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )


def load_gold_results(gold_file):
    questions = []
    question = {}
    answers = []
    with open(gold_file, mode="r", encoding="UTF-8") as gold_answers:
        for line in gold_answers:
            line = line.replace("\n", "")
            if line.startswith("Frase"):
                if question:
                    question["answers"] = answers
                    question["answer_size"] = len(answers)
                    questions.append(question)
                    question = {}
                    answers = []

                question["id"] = len(questions)
                question["question"] = line.split(": ")[1]
            else:
                answer = json.loads(line)
                answers.append([answer["subject"], answer["predicate"], answer["object"]])



    return questions


# analised_qald7 = []
qald7 = load_gold_results("../phrases/respostasEnsepro4Qald.gold")
#
# for question in qald7["questions"]:
#     analised = {}
#     analised["id"] = question["id"]
#     analised["question"] = extract_pt_question(question["question"])
#
#     answer_location = get_answer_location(question)
#     analised["is_boolean"] = answer_location == "boolean"
#
#     answers = []
#     if not analised["is_boolean"]:
#         answers = extract_and_normalize_answer(question["answers"], answer_location)
#         analised["answers"] = answers
#
#     analised["answer_size"] = len(answers)
#     analised_qald7.append(analised)
#
#     """
#     {
#     "question": ""
#     "answer_size": 1
#     "is_boolean": True/False
#     "answers":[
#     ]
#     }
#
#     """

save_as_json(qald7, "../phrases/analised_qald7_pt.json")
