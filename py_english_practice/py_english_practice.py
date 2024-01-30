import random
import sentence_to_translate
import json
import os


def display_welcome_message():
    print("""   Bienvenue dans le Quiz d'Anglais!
    - Choisissez de commencer le quiz ou de consulter votre historique d'erreurs.
    - Répondez aux questions en traduisant des phrases du français vers l'anglais.
    - Recevez des feedbacks et consultez votre performance.
    """)

def view_history():
    try:
        with open("error_history.json", "r") as file:
            errors_dict = json.load(file)
    except FileNotFoundError:
        print("\n⚠️ Aucun historique d’erreur trouvé.\n")
        return
    except json.JSONDecodeError:
        print("\n⚠️ Erreur de lecture du fichier JSON. Le fichier est peut-être corrompu.\n")
        return

    sorted_errors = sorted(errors_dict.items(), key=lambda item: item[1]['count'], reverse=True)

    print(f"\n{'Nb erreurs':<11} | {'Français': <60} | {'Anglais': <60}")
    print("-"*110)

    for french_sentence, details in sorted_errors:
        nb_errors = details['count']
        english_sentence = details['en']
        print(f"{nb_errors: <11} | {french_sentence: <60} | {english_sentence: <60}")

def display_quiz_text(text):
    ascii_border = """
    *******************
    * {} *
    *******************
    """.format(text)
    print(ascii_border)

def save_errors_to_json(new_errors, filename="error_history.json"):
    try:
        if os.path.exists(filename):
            with open(filename, "r") as file:
                existing_errors = json.load(file)
            for key, value in new_errors.items():
                if key in existing_errors:
                    existing_errors[key]['count'] += value['count']
                else:
                    existing_errors[key] = value
        else:
            existing_errors = new_errors

        with open(filename, "w") as file:
            json.dump(existing_errors, file, indent=4, ensure_ascii=False)
    except (IOError, OSError) as e:
        print(f"\n⚠️ Erreur d’écriture du fichier: {e}\n")

def start_quiz():
    while True:
        try:
            feedback_mode = int(input("Choisissez votre mode de feedback : \n1. 'immédiat' pour un retour après chaque question.\n0. 'final' pour un récapitulatif à la fin.\n: "))
            if feedback_mode in [0, 1]:
                break
            else:
                print("\n⚠️ Entrée invalide. Veuillez choisir 1 ou 0.\n")
        except ValueError:
                print("\n⚠️ Entrée invalide. Veuillez entrer un nombre (1 ou 0).\n")

    user_category = get_user_category()

    while True:
        try:
            number_of_questions = int(input("Combien de questions voulez-vous? \n: "))
            if number_of_questions > 0:
                break
            else:
                print("\n⚠️ Entrée invalide. Veuillez entrer un nombre positif.\n")
        except ValueError:
            print("\n⚠️ Entrée invalide. Veuillez entrer un nombre entier, par exemple 1 ou 2.\n")

    if user_category == "all":
        sentences = []
        for category in sentence_to_translate.get_categories():
            sentences.extend(sentence_to_translate.get_sentences(category))
    else:
        sentences = sentence_to_translate.get_sentences(user_category)

    selected_sentences = random.sample(sentences, min(number_of_questions, len(sentences)))


    display_quiz_text("  Quiz Start   ")

    correct_answer = 0
    incorrect_answers_dic = {}

    for i, sentence in enumerate(selected_sentences, 1):
        print(f"\n{i}. {sentence['fr']}")
        user_answer = input(": ")
        if user_answer == sentence['en']:
            print("✅ Correct!")
            correct_answer += 1
        else:
            if feedback_mode:
                print(f": {sentence['en']}")
            print("❌ Incorrect!")
            incorrect_answers_dic[sentence['fr']] = {'en': sentence['en'], 'count':1}

    save_errors_to_json(incorrect_answers_dic)
    display_quiz_text("   Quiz End    ")
    print(f"\nNombre de bonnes réponses : {correct_answer}/{number_of_questions}")

    if incorrect_answers_dic:
        print("\nDétail des erreurs :")
        for i, (french_sentence, details) in enumerate(incorrect_answers_dic.items(), start=1):
            english_translation = details['en']
            print(f"{i}. {french_sentence}\n>> {english_translation}\n")



def get_user_category():
    categories = sentence_to_translate.get_categories()
    print("Chosissez une catégorie de phrases à traduire : ")
    print("0. Toutes les catégories")
    for index, category in enumerate(categories,1):
        print(f"{index}. {category}")

    while True:
        try:
            choice = int(input(": "))
            if 0 <= choice <= len(categories):
                    return "all" if choice == 0 else categories[choice - 1]
            else:
                print(f"\n⚠️ Entrée invalide. Veuillez choisir un nombre entre 0 et {len(categories)}\n")
        except ValueError:
            print(f"\n⚠️ Entrée invalide. Veuillez choisir un nombre entre 0 et {len(categories)}\n")



def get_user_mode():
    while True:
        try:
            mode = int(input("***********************\nChoisissez une option : \n1. Commencer le Quiz\n0. Consulter l’historique des erreurs\n: "))
            if mode in [0,1]:
                return mode
            print("\n⚠️ Entrée invalide. Veuillez choisir 1 ou 0\n")
        except ValueError:
            print("\n⚠️ Entrée invalide. Veuillez entrer un nombre (1 ou 0)\n")

def main():
    display_quiz_text("WordBridge Quiz")
    display_welcome_message()
    while True:
        user_mode = get_user_mode()

        if user_mode:
            start_quiz()
        else:
            view_history()

        while True:
            try:
                restart = int(input("\n***********************\nVoulez-vous revenir au menu principal ?\n1. Oui\n0. Non\n: "))
                if restart not in [0, 1]:
                    print("\n⚠️ Entrée invalide. Veuillez choisir 1 ou 0\n")
                    continue
                break
            except ValueError:
                print("\n⚠️ Entrée invalide. Veuillez entrer un nombre (1 ou 0)\n")

        if restart == 0:
            print("\nMerci d’avoir utilisé le quiz. Au revoir.")
            break
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")