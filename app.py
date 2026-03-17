from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)


products = [
    {
        "name":"Bouteille de 1L",
        "description":"Petite boutielle en plastique qui est légère et adapté au stockage de l'eau."
    },
    {
        "name":"Capsule de café en aluminium",
        "description":"Petite capsule de café compatible avec les machines à café Nespreso."
    },
    {
        "name":"Machine de remplissage",
        "description":"Machine permettant de remplir de contenant au niveau industriel."
    },
    {
        "name":"Convoyeur industriel",
        "description":"Système de transport automatiser pour ligne de production"
    },
]

conversation_history = []


@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/chat", methods=["post"])
def chat():
    #debut de la demande utilisateur et tri afin de pouvoir faire un pret tri part rapport au mot utliliser dans la question en comparaison avec le nom et la description des produits
    try:
        user_message = request.json.get("message", "")
        print("MESSAGE UTILISATEUR :", user_message)

        conversation_history.append(f"Utilisateur : {user_message}")
        conversation_history[:] = conversation_history[-6:]

        user_words = set(user_message.lower().split())

        print("USER WORD + : ", user_words)
        lists_products = []

        for p in products:
            products_text = (p["name"] + ' ' + p["description"]).lower()
            products_words = set(products_text.split())
            if user_words & products_words:
                lists_products.append(p)

        print("PRODUCT WORD FINALE :", lists_products)

        if lists_products:
            context = "\n".join(
                [f"- {p['name']}: {p['description']}" for p in lists_products]
            )
        else:
            context = "\n".join(
                [f"- {p['name']}: {p['description']}" for p in products]
            )
        #envoie sois la liste préséletionné des article potentielemnt interessant a l'IA selon les mots utliser dans la question du client, si aucun mots ne correspond, c'est a l'IA de determiner par rapport a la liste de produit complète.
        print("CONTEXT :")
        print(context)

        history_text = "\n".join(conversation_history)

# creation du prompt avec la question utilisateur
        prompt = f"""
Tu es un assistant e-commerce pour une plateform industrielle.
Tu aides un client à comprendre les produits disponibles tu va recevoir la liste des produit présélectionner pour le client tu devra determiner lequel est le plus pertinent pour lui. 

Produits disponibles : 
{context}

Historique de conversation :
{history_text}

Question du client : 
{user_message}

Répond de facon simple, claire et utile.
Si possible recommande un produit de la liste.
"""

        print("PROMPT ENVOYER :")
        print(prompt)

# creation de la demande a llama3, creation du json a utliser avec flask
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        print("STATUS CODE :", response.status_code)
        print("MESSAGE BRUTE :", response.text)

        response.raise_for_status()

        data = response.json()
        print("JSON PARSE :", data)

        answer = data.get("response", "Aucune reponse générée.")

        conversation_history.append(f"Assistant : {answer}")
        conversation_history[:] = conversation_history[-6:]

        return jsonify({"answer": answer})
# creation de la reponse 
    
# gestion des erreurs

    except Exception as e:
        print("ERREUR DETAILLE :", repr(e))
        return jsonify({
            "answer": f"Erreur lors de l'appel au modèle : {str(e)}"
        })
    
#ajout d'une barre de recherche, logique de check les produits existatn
@app.route("/search", methods=["post"])
def search():
    try:
        query = request.json.get("query", "").lower().strip()
        print("RECHERCHE : ", query)

        if query == "":
            return jsonify({"results": products})
        
        filter_product = []

        for p in products:
            name = p["name"].lower()
            description = p["description"].lower()

            if query in name or query in description:
                filter_product.append(p)
        return jsonify ({"results": filter_product})

    except Exception as e:
        print("ERREUR DETAILLE :", repr(e))
        return jsonify({"results": [], "error": str(e)})

#permet de clear tout l'historique de conversation    
@app.route("/reset_chat", methods=["POST"])
def reset_chat():
    conversation_history.clear()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
