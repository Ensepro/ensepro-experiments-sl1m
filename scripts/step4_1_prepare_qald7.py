import json


def save_as_json(value, filename, indent=2, sort_keys=False):
    print(
        json.dumps(value, indent=indent, sort_keys=sort_keys, ensure_ascii=False),
        file=open(filename, mode='w', encoding="UTF-8"),
        flush=True
    )


def load_json(file):
    return json.loads(open(file=file, mode="r", encoding="utf-8").read())


def extract_pt_question(lang_questions):
    for lang in lang_questions:
        if lang["language"] == "pt_BR":
            return lang["string"]
    raise Exception("should not happen", 1)


def get_answer_location(question):
    if question["answers"][0]["results"]:
        return "results"
    elif "boolean" in question["answers"][0]:
        return "boolean"


def get_gold_answer_size(question, answer_in):
    if answer_in == "boolean":
        return 1
    elif answer_in == "results":
        return len(question["answers"][0]["results"])
    else:
        return -1


def extract_and_normalize_answer(answers, location):
    output = []
    if location == "results":
        for bindings in answers[0]["results"]["bindings"]:
            for bind in bindings:
                if bind in ["uri", "date", "string", "list", "c"]:
                    value = bindings[bind]["value"].lower()
                    value = value.replace("http://dbpedia.org/resource/", "")
                    value = value.replace("(", "").replace(")", "")
                    output.append(value)
                else:
                    print(bind)
    return output


analised_qald7 = []
qald7 = load_json("../phrases/qald7.json")

for question in qald7["questions"]:
    analised = {}
    analised["id"] = question["id"]
    analised["question"] = extract_pt_question(question["question"])

    answer_location = get_answer_location(question)
    analised["is_boolean"] = answer_location == "boolean"

    answers = []
    if not analised["is_boolean"]:
        answers = extract_and_normalize_answer(question["answers"], answer_location)
        analised["answers"] = answers

    analised["answer_size"] = len(answers)
    analised_qald7.append(analised)

    """
    {
    "question": ""
    "answer_size": 1
    "is_boolean": True/False
    "answers":[
    ]
    }
    
    """

save_as_json(analised_qald7, "../phrases/analised_qald7.json")
