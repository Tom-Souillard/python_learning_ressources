import sentence_to_translate

def get_user_category():
    categories = sentence_to_translate.get_categories()
    print("Chosissez une catégorie : ")
    print("0. Toutes les catégories")
    for index, category in enumerate(categories,1):
        print(f"{index}. {category}")

    while True:
        try:
            choice = int(input(": "))
            if 0 <= choice <= len(categories):
                return choice
            else:
                print(f"Entrée invalide. Veuillez choisir un nombre entre 0 et {len(categories)}")
        except ValueError:
            print(f"Entrée invalide. Veuillez choisir un nombre entre 0 et {len(categories)}")



def get_user_mode():
    while True:
        try:
            mode = int(input("Choisissez une option : \n0. Commencer le Quiz\n1. Consulter l’historique des erreurs\n: "))
            if mode in [0,1]:
                return mode
            print("Entrée invalide. Veuillez choisir 0 ou 1")
        except ValueError:
            print("Entrée invalide. Veuillez choisir 0 ou 1")

def main():
    print("Bienvenue dans le Quiz d’anglais")
    user_mode = get_user_mode()
    user_category = get_user_category()


if __name__ == "__main__":
    main()