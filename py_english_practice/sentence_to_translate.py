# Dictionnaire des phrases à traduire par catégorie

sentence_to_translate = {
    "Quotidien": [
        {"fr": "Quel temps fait-il aujourd'hui ?", "en": "What is the weather like today?"},
        {"fr": "Je vais faire des courses au supermarché.", "en": "I am going shopping at the supermarket."}
    ],
    "Professionnel": [
        {"fr": "Bonjour, je suis heureux de vous rencontrer.", "en": "Hello, I am pleased to meet you."},
        {"fr": "Pouvez-vous m'envoyer le rapport avant vendredi ?", "en": "Can you send me the report before Friday?"}
    ],
    "Petite enfance": [
        {"fr": "Les enfants jouent dans le parc.", "en": "The children are playing in the park."},
        {"fr": "Il est l'heure d'aller au lit.", "en": "It is time to go to bed."}
    ]
}

def get_categories():
    """"
    Retourne la liste des catégories disponibles.
    """
    return list(sentence_to_translate.keys())

def get_sentences(category):
    """
    Renvoie une liste de phrases de la catégorie spécifiée.
    """
    return sentence_to_translate.get(category,[])