from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'ton_secret_key'  # Nécessaire pour les messages flash

# Chemin vers les fichiers JSON
DATA_DIR = os.path.join(os.path.dirname(__file__), 'static', 'data')
INGREDIENTS_FILE = os.path.join(DATA_DIR, 'ingredients.json')
RECETTES_FILE = os.path.join(DATA_DIR, 'recettes.json')
MENU_FILE = os.path.join(DATA_DIR, 'menu-semaine.json')

# Fonction pour charger les données
def load_data(file_path, key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file).get(key, {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Fonction pour sauvegarder les données
def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour afficher les ingrédients
@app.route('/ingredients')
def liste_ingredients():
    # Charger les ingrédients depuis le fichier JSON
    ingredients = load_data(INGREDIENTS_FILE, 'ingredients')

    # Récupérer la catégorie sélectionnée depuis les paramètres de requête
    selected_category = request.args.get('categorie')

    return render_template('ingredients/liste_ingredients.html', ingredients=ingredients, selected_category=selected_category)

# Route pour ajouter un ingrédient
@app.route('/ingredients/ajouter', methods=['GET', 'POST'])
def ajouter_ingredient():
    if request.method == 'POST':
        category = request.form['category']
        new_item = request.form['nom']

        ingredients = load_data(INGREDIENTS_FILE, 'ingredients')
        if category in ingredients:
            ingredients[category].append(new_item)
        else:
            ingredients[category] = [new_item]

        save_data(INGREDIENTS_FILE, {"ingredients": ingredients})
        return redirect(url_for('liste_ingredients'))

    categories = load_data(INGREDIENTS_FILE, 'ingredients').keys()
    return render_template('ingredients/ajouter_ingredient.html', categories=categories)

# Routes pour les recettes
@app.route('/recettes')
def liste_recettes():
    recettes = load_data(RECETTES_FILE, 'recettes')
    return render_template('recettes/liste_recettes.html', recettes=recettes)

@app.route('/recettes/<int:id>')
def details_recette(id):
    recettes = load_data(RECETTES_FILE, 'recettes')
    if 0 <= id < len(recettes):
        recette = recettes[id]
        return render_template('recettes/details_recette.html', recette=recette)
    else:
        flash('Recette non trouvée.', 'error')
        return redirect(url_for('liste_recettes'))

@app.route('/recettes/ajouter', methods=['GET', 'POST'])
def ajouter_recette():
    if request.method == 'POST':
        try:
            nom = request.form['nom']
            categorie = request.form['categorie']
            personnes = int(request.form['personnes'])
            difficulte = request.form['difficulte']
            image = request.form['image']
            temps_cuisson = int(request.form['temps_cuisson'])

            noms_ingredients = request.form.getlist('ingredient_nom[]')
            quantites_ingredients = request.form.getlist('ingredient_quantite[]')
            unites_ingredients = request.form.getlist('ingredient_unite[]')

            etapes = request.form.getlist('etape[]')

            ingredients = []
            for nom, quantite, unite in zip(noms_ingredients, quantites_ingredients, unites_ingredients):
                ingredients.append({
                    "nom": nom,
                    "quantite": float(quantite),
                    "unite": unite
                })

            nouvelle_recette = {
                "nom": nom,
                "categorie": categorie,
                "personnes": personnes,
                "difficulte": difficulte,
                "image": image,
                "temps_cuisson": temps_cuisson,
                "ingredients": ingredients,
                "etapes": etapes
            }

            recettes = load_data(RECETTES_FILE, 'recettes')
            recettes.append(nouvelle_recette)
            save_data(RECETTES_FILE, {"recettes": recettes})

            flash('Recette ajoutée avec succès!', 'success')
            return redirect(url_for('liste_recettes'))

        except (KeyError, ValueError) as e:
            flash('Erreur dans les données du formulaire.', 'error')
            return redirect(url_for('ajouter_recette'))

    ingredients = load_data(INGREDIENTS_FILE, 'ingredients')
    return render_template('recettes/ajouter_recette.html', ingredients=ingredients)

@app.route('/recettes/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_recette(id):
    recettes = load_data(RECETTES_FILE, 'recettes')
    if 0 <= id < len(recettes):
        recette = recettes[id]

        if request.method == 'POST':
            recette['nom'] = request.form['nom']
            recette['categorie'] = request.form['categorie']
            recette['personnes'] = int(request.form['personnes'])
            recette['difficulte'] = request.form['difficulte']
            recette['image'] = request.form['image']
            recette['temps_cuisson'] = int(request.form['temps_cuisson'])

            recette['ingredients'] = []
            noms_ingredients = request.form.getlist('ingredient_nom[]')
            quantites_ingredients = request.form.getlist('ingredient_quantite[]')
            unites_ingredients = request.form.getlist('ingredient_unite[]')

            for nom, quantite, unite in zip(noms_ingredients, quantites_ingredients, unites_ingredients):
                recette['ingredients'].append({
                    "nom": nom,
                    "quantite": float(quantite),
                    "unite": unite
                })

            recette['etapes'] = request.form.getlist('etape[]')
            save_data(RECETTES_FILE, {"recettes": recettes})

            flash('Recette modifiée avec succès!', 'success')
            return redirect(url_for('liste_recettes'))

        return render_template('recettes/modifier_recette.html', recette=recette, id=id)

    else:
        flash('Recette non trouvée.', 'error')
        return redirect(url_for('liste_recettes'))

@app.route('/recettes/supprimer/<int:id>')
def supprimer_recette(id):
    recettes = load_data(RECETTES_FILE, 'recettes')
    if 0 <= id < len(recettes):
        recettes.pop(id)
        save_data(RECETTES_FILE, {"recettes": recettes})
        flash('Recette supprimée avec succès.', 'success')
    else:
        flash('Recette non trouvée.', 'error')
    return redirect(url_for('liste_recettes'))

# Routes pour le planning
@app.route('/planning')
def afficher_planning():
    menus = load_data(MENU_FILE, 'menus')
    recettes = load_data(RECETTES_FILE, 'recettes')
    return render_template('menu/planning.html', menus=menus, recettes=recettes)

@app.route('/planning/ajouter', methods=['POST'])
def ajouter_planning():
    # Récupérer les données du formulaire
    jour = request.form['jour']
    moment = request.form['moment']
    recette = request.form.getlist('recette')
    ingredients = request.form.getlist('ingredients')  # Récupérer la liste des ingrédients

    # Charger les données existantes
    menus = load_data(MENU_FILE, 'menus')

    # Vérifier si le jour existe déjà dans le planning
    if jour not in menus:
        menus[jour] = {}

    # Ajouter la recette et les ingrédients au planning
    menus[jour][moment] = {
        'recette': recette,
        'ingredients': ingredients  # Associer les ingrédients à la recette
    }

    # Sauvegarder les données mises à jour
    save_data(MENU_FILE, {"menus": menus})

    # Afficher un message de succès
    flash('Recette et ingrédients ajoutés avec succès!', 'success')

    # Rediriger vers la page du planning
    return redirect(url_for('afficher_planning'))

@app.route('/planning/supprimer/<string:jour>')
def supprimer_planning(jour):
    menus = load_data(MENU_FILE, 'menus')
    if jour in menus:
        del menus[jour]
        save_data(MENU_FILE, {"menus": menus})
        flash('Planning supprimé avec succès.', 'success')
    else:
        flash('Jour non trouvé.', 'error')
    return redirect(url_for('afficher_planning'))

@app.route('/reinitialiser_planning', methods=['POST'])
def reinitialiser_planning():
    save_data(MENU_FILE, {"menus": {}})
    flash('Le menu a été réinitialisé avec succès.', 'success')
    return redirect(url_for('afficher_planning'))

if __name__ == '__main__':
    app.run(debug=True)