from flask import Flask, render_template, request, redirect, url_for, flash
from data_utils import load_data, save_data, INGREDIENTS_FILE, RECETTES_FILE, MENU_FILE
from functools import wraps
import uuid

# Constantes globales
CATEGORIES = [
    "Entrée", "Viande", "Charcuterie", "Poisson", "Légumes", "Féculents", 
    "Dessert fromage", "Epices et condiments base", "Gouter et petit dejeuner", "test"
]

SOUS_CATEGORIES = {
    "Entrée": ["Cakes salés", "Entrées chaudes", "Entrées chaudes", "Quiches", "Tartes", "Sandwichs"],
    "Viande": ["Viandes rouges", "Viandes blanches", "Viandes noires"],
    "Charcuterie": ["Viandes rouges", "Viandes blanches", "Viandes noires"],
    "Poisson": ["Poissons pour grillade/poele", "Poissons cuisson vapeur", "Poisson gras", "Poisson maigres", "Poisson pour soupes"],
    "Légumes": ["Légumes racines", "Légumes-feuilles", "Légumes crucifères", "Légumes à fruits", "Légumes verts", "Légumes à fleurs", "Légumes à exotique"],
    "Féculents": ["Céréales", "Légumineuses", "Tubercules", "Pain", "Semoules/farines"],
    "Dessert & fromage": ["Fruits", "Produits laitiers", "Fromages"],
    "Epices et condiments base": ["Herbes séchées", "Mélanges d'épices", "Condiments salés", "Condiments sucrés", "Condiments acides"],
    "Gouter et petit dejeuner": ["Pâtisseries", "Céréales", "Pâtes à tartiner", "Boissons chaudes", "Jus/Sirop"]
}

UNITES = ["pièces", "kg", "g", "L", "mL", "cL","Cuillère à café", "Cuillère à soupe", 
    "tasse", "verre", "pincée", "sachet", "boîte", "bouteille", "portion"
]

# Fonctions utilitaires
def generate_unique_id():
    return str(uuid.uuid4())

def get_ingredients():
    return load_data(INGREDIENTS_FILE, 'ingredients')

def save_ingredients(ingredients):
    save_data(INGREDIENTS_FILE, {'ingredients': ingredients})

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            flash(f'Une erreur est survenue : {str(e)}', 'error')
            return redirect(url_for('index'))
    return wrapper

# Fonctions pour manipuler les ingrédients
def add_ingredient(nom, categorie, sous_categorie, unite, calories, alternatives):
    """
    Ajoute un nouvel ingrédient à la liste des ingrédients et sauvegarde les données.
    """
    ingredients = get_ingredients()
    nouvel_ingredient = {
        "id": generate_unique_id(),
        "nom": nom,
        "catégorie": categorie,
        "sous_catégorie": sous_categorie,
        "unité": unite,
        "calories": int(calories) if calories else 0,
        "alternatives": alternatives
    }
    ingredients.append(nouvel_ingredient)
    save_ingredients(ingredients)

def update_ingredient(ingredient, nom, categorie, sous_categorie, unite, calories, alternatives):
    """
    Met à jour un ingrédient existant et sauvegarde les données.
    """
    ingredient['nom'] = nom
    ingredient['catégorie'] = categorie
    ingredient['sous_catégorie'] = sous_categorie
    ingredient['unité'] = unite
    ingredient['calories'] = int(calories) if calories else 0
    ingredient['alternatives'] = alternatives
    save_ingredients(get_ingredients())

def delete_ingredient(id):
    """
    Supprime un ingrédient de la liste et sauvegarde les données.
    """
    ingredients = get_ingredients()
    ingredients = [item for item in ingredients if item['id'] != id]
    save_ingredients(ingredients)

# Application Flask
app = Flask(__name__)
app.secret_key = 'ton_secret_key'

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingredients')
@handle_errors
def liste_ingredients():
    ingredients_data = get_ingredients()
    ingredients = {}
    for item in ingredients_data:
        category = item['catégorie']
        if category not in ingredients:
            ingredients[category] = []
        ingredients[category].append(item)
    selected_category = request.args.get('categorie')
    return render_template('ingredients/liste_ingredients.html', ingredients=ingredients, selected_category=selected_category)

@app.route('/ajouter_ingredient', methods=['GET', 'POST'])
@handle_errors
def ajouter_ingredient():
    if request.method == 'POST':
        nom = request.form.get('nom')
        categorie = request.form.get('categorie')
        sous_categorie = request.form.get('sous_categorie')
        unite = request.form.get('unite')
        calories = request.form.get('calories')
        alternatives = request.form.get('alternatives').split(',')

        if not nom or not categorie:
            flash('Le nom et la catégorie sont obligatoires.', 'error')
            return redirect(url_for('ajouter_ingredient'))

        add_ingredient(nom, categorie, sous_categorie, unite, calories, alternatives)
        flash('Ingrédient ajouté avec succès.', 'success')
        return redirect(url_for('liste_ingredients', categorie=categorie))

    return render_template('ingredients/ajouter_ingredient.html', categories=CATEGORIES, sous_categories=SOUS_CATEGORIES, unites=UNITES)

@app.route('/modifier_ingredient/<string:id>', methods=['GET', 'POST'])
@handle_errors
def modifier_ingredient(id):
    ingredients = get_ingredients()
    ingredient = next((item for item in ingredients if item['id'] == id), None)

    if not ingredient:
        flash('Ingrédient non trouvé.', 'error')
        return redirect(url_for('liste_ingredients'))

    if request.method == 'POST':
        update_ingredient(ingredient, request.form.get('nom'), request.form.get('categorie'), request.form.get('sous_categorie'), request.form.get('unite'), request.form.get('calories'), request.form.get('alternatives').split(','))
        flash('Ingrédient modifié avec succès.', 'success')
        return redirect(url_for('liste_ingredients'))

    return render_template('ingredients/modifier_ingredient.html', ingredient=ingredient, categories=CATEGORIES, sous_categories=SOUS_CATEGORIES, unites=UNITES)

@app.route('/supprimer_ingredient/<string:id>', methods=['POST'])
@handle_errors
def supprimer_ingredient(id):
    delete_ingredient(id)
    flash('Ingrédient supprimé avec succès.', 'success')
    return redirect(url_for('liste_ingredients'))

if __name__ == '__main__':
    app.run(debug=True)