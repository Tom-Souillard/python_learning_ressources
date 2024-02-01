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


def start_quiz():
    print("Hello")
def view_history():
    errors_dict = FileManager.read_json("error_history.json")
    sorted_errors = sorted(errors_dict.items(), key=lambda item: item[1]['count'], reverse=True)

    

def main():
    QuizInterface.display_quiz_text("WordBridge Quiz")
    QuizInterface.display_welcome_message()

    while True:
        user_mode = QuizInterface.get_user_input("***********************\nChoisissez une option : \n1. Commencer le Quiz\n0. Consulter l’historique des erreurs\n: ", [0, 1])
        if user_mode:
            start_quiz()
        else:
            view_history()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n⚠️ Une erreur inattendue est survenue : {e}\n")