import json
import questions


def get_user_mode():
    while True:
        try:
            mode = int(input("Choisissez le mode de jeu (1 pour QCM, 0 pour réponse manuelle): "))
            if mode in [0, 1]:
                return mode
            print("Entrée invalide. Veuillez choisir 0 ou 1.")
        except ValueError:
            print("Entrée invalide. Veuillez choisir 0 ou 1.")


def get_user_category():
    categories = list(questions.questions.keys())
    while True:
        print("Choisissez une catégorie : ")
        for index, category in enumerate(categories, 1):
            print(f"{index}. {category}")
        print("0. Toutes les catégories")
        choice = int(input("Votre choix : "))
        if 0 <= choice <= len(categories):
            return None if choice == 0 else categories[choice - 1]
        print(f"Veuillez choisir un nombre entre 0 et {len(categories)}.")


def ask_question(question, options):
    print(question)
    for key, option in options.items():
        print(f"{key}. {option}")
    while True:
        try:
            response = int(input("Votre réponse : "))
            if 1 <= response <= 4:
                return response
            print("Entrée invalide. Veuillez choisir un nombre entre 1 et 4.")
        except ValueError:
            print("Entrée invalide. Veuillez choisir un nombre entre 1 et 4.")


def main():
    user_mode = get_user_mode()
    user_category = get_user_category()

    if user_category:
        selected_questions = questions.questions[user_category]
    else:
        selected_questions = {k: v for cat in questions.questions.values() for k, v in cat.items()}

    correct_answers = 0
    incorrect_answers = []

    for question, details in selected_questions.items():
        user_answer = ask_question(question, details["options"])
        if user_answer == details["answer"]:
            print("Correct!")
            correct_answers += 1
        else:
            print("Incorrect!")
            incorrect_answers.append({
                "question": question,
                "your_answer": details["options"][user_answer],
                "correct_answer": details["options"][details["answer"]],
                "explanation": details["explanation"]
            })

    # Sauvegarde de l'historique
    with open("history.json", "a") as history_file:
        history_data = {
            "category": user_category or "Toutes les catégories",
            "correct": correct_answers,
            "incorrect": len(incorrect_answers),
            "details": incorrect_answers
        }
        json.dump(history_data, history_file)
        history_file.write('\n')

    # Récapitulatif
    print(f"\nNombre de bonnes réponses : {correct_answers}")
    print(f"Nombre de mauvaises réponses : {len(incorrect_answers)}")
    if incorrect_answers:
        print("\nDétail des erreurs :")
        for error in incorrect_answers:
            print(f"Question : {error['question']}")
            print(f"Votre réponse : {error['your_answer']}")
            print(f"Réponse correcte : {error['correct_answer']}")
            print(f"Explication : {error['explanation']}\n")


if __name__ == "__main__":
    main()
