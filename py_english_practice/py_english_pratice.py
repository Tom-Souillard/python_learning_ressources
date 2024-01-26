def get_user_mode():
    while True:
        try:
            mode = int(input("Choisissez une option : \n1. Commencer le Quiz\n2. Consulter l’historique des erreurs\n: "))
            if mode in [0,1]:
                return mode
            print("Entrée invalide. Veuillez choisir 0 ou 1")
        except ValueError:
            print("Entrée invalide. Veuillez choisir 0 ou 1")

def main():
    print("Bienvenue dans le Quiz d’anglais")
    user_mode = get_user_mode()

if __name__ == "__main__":
    main()