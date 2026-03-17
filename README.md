# mini-assistant-e-commerce-IA

# Assistant IA pour mini plateforme e-commerce

Prototype d'un assistant conversationnel utilisant un LLM pour aider un utilisateur à trouver des produits industriels.

## Fonctionnalités

- recherche produit par mots-clés
- assistant conversationnel avec IA (Ollama / Llama3)
- filtrage des produits selon la question utilisateur
- historique de conversation
- interface web simple avec Flask

## Technologies

- Python
- Flask
- JavaScript
- HTML / CSS
- API LLM (Ollama)

## Architecture

Utilisateur
↓
Interface Web (HTML / JavaScript)
↓
Flask Backend
↓
API Ollama
↓
LLM (Llama3)

## Installation

## Installation du modèle IA

Ce projet utilise **Ollama** pour exécuter un modèle de langage local.

### Installer Ollama

https://ollama.com/

``bash
ollama pull llama3
##verifier que le model fonctionne
ollama run llama3

### Télécharger le modèle

```bash
git clone https://github.com/brachidios720/mini-assistant-ecommerce-ai
cd mini-assistant-ecommerce-ai
pip install -r requirements.txt
python app.py

go to : http://127.0.0.1:5000
