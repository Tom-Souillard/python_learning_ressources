import random
import sentence_to_translate
import json
import os

class QuizInterface:
    @staticmethod
    def display_quiz_text(prompt):
        ascii_border = f"""
        *******************
        * {prompt} *
        *******************
        """
        print(ascii_border)

    @staticmethod
    def display_welcome_message():
        print("""   Bienvenue dans le Quiz d'Anglais!
        - Choisissez de commencer le quiz ou de consulter votre historique d'erreurs.
        - Répondez aux questions en traduisant des phrases du français vers l'anglais.
        - Recevez des feedbacks et consultez votre performance.
        """)

    @staticmethod
    def get_user_input(prompt, valid_options):
        while True:
            try:
                user_input = int(input(prompt))
                if user_input in valid_options:
                    return user_input
                else:
                    print(f"\n⚠️ Entrée invalide. Veuillez choisir parmi {valid_options}\n")
            except ValueError:
                print(f"\n⚠️ Entrée invalide. Veuillez entrer un nombre parmi {valid_options}\n")


class FileManager:
    @staticmethod
    def read_json(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("\n⚠️ Aucun historique d’erreur trouvé.\n")
            return {}
        except json.JSONDecodeError:
            print("\n⚠️ Erreur de lecture du fichier JSON. Le fichier est peut-être corrompu.\n")
            return {}

    @staticmethod
    def save_errors_to_json(incorrect_answers_dic, filename="error_history.json"):
        try:
            if os.path.exists(filename):
                existing_errors = FileManager.read_json(filename)
                for key, value in incorrect_answers_dic.items():
                    if key in existing_errors:
                        existing_errors[key]['count'] += value['count']
                    else:
                        existing_errors[key] = value
            else:
                existing_errors = incorrect_answers_dic

            with open(filename, "w") as file:
                json.dump(existing_errors, file, indent=4, ensure_ascii=False)
        except (IOError, OSError) as e:
            print(f"\n⚠️ Erreur d’écriture du fichier: {e}\n")

class Quiz:
    def __init__(self, selected_sentences, feedback_mode):
        self.selected_sentences = selected_sentences
        self.feedback_mode = feedback_mode
        self.correct_answers = 0
        self.incorrect_answers_dic = {}

    def start(self):
        QuizInterface.display_quiz_text("  Quiz Start   ")
        for i, sentence in enumerate(self.selected_sentences,1):
            print(f"\n{i}. {sentence['fr']}")
            user_answer = input(": ")
            if user_answer == sentence['en']:
                print("✅ Correct!")
                self.correct_answers += 1
            else:
                if self.feedback_mode:
                    print(f": {sentence['en']}")
                print("❌ Incorrect!")
                self.incorrect_answers_dic[sentence['fr']] = {'en': sentence['en'], 'count':1}

        FileManager.save_errors_to_json(self.incorrect_answers_dic)
        QuizInterface.display_quiz_text("   Quiz End    ")
        self.display_result()

    def display_result(self):
        print(f"\nNombre de bonnes réponses : {self.correct_answers}/{len(self.selected_sentences)}")
        print("\nDétail des erreurs :")
        for i, (french_sentence, details) in enumerate(self.incorrect_answers_dic.items(), start=1):
            english_translation = details['en']
            print(f"{i}. {french_sentence}\n>> {english_translation}\n")

def setup_and_launch_quiz ():
    feedback_mode = QuizInterface.get_user_input("Choisissez votre mode de feedback : \n1. 'immédiat' pour un retour après chaque question.\n0. 'final' pour un récapitulatif à la fin.\nVotre choix : ", [0, 1])
    user_category = get_user_category()
    number_of_questions = QuizInterface.get_user_input("Combien de questions voulez-vous? \n: ", range(1, 1001))

    if user_category == "all":
        sentences = []
        for category in sentence_to_translate.get_categories():
            sentences.extend(sentence_to_translate.get_sentences(category))
    else:
        sentences = sentence_to_translate.get_sentences(user_category)

    selected_sentences = random.sample(sentences, min(number_of_questions, len(sentences)))
    quiz = Quiz(selected_sentences, feedback_mode)
    quiz.start()

def get_user_category():
    categories = sentence_to_translate.get_categories()
    print("Choisissez une catégorie de phrases à traduire : ")
    print("0. Toutes les catégories")
    for index, category in enumerate(categories, 1):
        print(f"{index}. {category}")
    choice = QuizInterface.get_user_input(": ", list(range(len(categories) + 1)))
    return "all" if choice == 0 else categories[choice - 1]

def view_history():
    errors_dict = FileManager.read_json("error_history.json")
    sorted_errors = sorted(errors_dict.items(), key=lambda item: item[1]['count'], reverse=True)

    print(f"\n{'Nb erreurs':<11} | {'Français': <60} | {'Anglais': <60}")
    print("-"*110)
    for french_sentence, details in sorted_errors:
        nb_errors = details['count']
        english_sentence = details['en']
        print(f"{nb_errors: <11} | {french_sentence: <60} | {english_sentence: <60}")

def main_menu():
    return QuizInterface.get_user_input(
        "***********************\n"
        "Choisissez une option :\n"
        "0. Consulter l’historique des erreurs\n"
        "1. Commencer le Quiz\n"
        "2. Quitter le jeu\n: ", [0, 1, 2])

def handle_history():
    view_history()
    return True  # Continue à afficher le menu principal

def handle_quiz():
    setup_and_launch_quiz()
    return True  # Continue à afficher le menu principal

def handle_exit():
    print("\nMerci d’avoir utilisé le quiz. Au revoir.")
    return False  # Quitte le programme

def main():
    QuizInterface.display_quiz_text("WordBridge Quiz")
    QuizInterface.display_welcome_message()

    action_handlers = {
        0: handle_history,
        1: handle_quiz,
        2: handle_exit
    }

    continue_running = True
    while continue_running:
        user_choice = main_menu()
        action_handler = action_handlers.get(user_choice)
        if action_handler:
            continue_running = action_handler()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n⚠️ Une erreur inattendue est survenue : {e}\n")