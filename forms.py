from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class IngredientForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    quantite = IntegerField('Quantité', validators=[DataRequired(), NumberRange(min=1)])
    unite = StringField('Unité', validators=[DataRequired()])

class RecetteForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    categorie = StringField('Catégorie', validators=[DataRequired()])
    personnes = IntegerField('Personnes', validators=[DataRequired(), NumberRange(min=1)])
    difficulte = StringField('Difficulté', validators=[DataRequired()])
    image = StringField('Image')
    temps_cuisson = IntegerField('Temps de cuisson (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    etapes = FieldList(StringField('Étape'), min_entries=1)
    submit = SubmitField('Enregistrer')