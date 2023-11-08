import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["question"]:
        if q["questions"] == question:
            return q["answer"]

def chatbot():
    knowledge_base = load_knowledge_base('knowledge_base.json')
    while True:
        user_input = input('You: ')
        if user_input.lower() == 'quit':  # Changed 'quit' to a string with quotes
            break
        best_match = find_best_match(user_input, [q["questions"] for q in knowledge_base["question"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know, please teach me.')
            new_answer = input("Type the answer or 'skip' to skip: ")
            if new_answer.lower() != 'skip':
                knowledge_base['question'].append({"questions": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you')

if __name__ == '__main__':
    chatbot()
