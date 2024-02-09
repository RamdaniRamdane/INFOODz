from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import requests


db = SQLAlchemy() #sqlalchemy c'est une orm de gestion de bd via flask 
bcrypt=Bcrypt() #fct resp du hashage des mdp avant de les stocker dans la bd



#fct qui cree l app avec ses configurations
def create_app():

    app = Flask (__name__)
    app.config['SECRET_KEY']='reyummto2023*'
    app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://admin:rey667.@localhost/reytest1"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['UPLOADED_PHOTOS_DEST'] = '/home/r3y0/programation/flaskpr/INFOOD/website/static/image'
    db.init_app(app)
    
    
    from .models import User
    create_database(app)


    #####view
    from .views import views

    views(app)

    return app





def create_database(app):
        from .models import User
        with app.app_context():
            db.create_all()   
            print('Created Database!')


def create_user(app, nom, prenom,username,wilaya, email ,password):
    from .models import User
    with app.app_context():
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(nom=nom,prenom=prenom,username=username,wilaya=wilaya, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            print("Utilisateur ajouté avec succès à la base de données.")
        else:
            print("L'utilisateur avec ce nom existe déjà.")


from .models import Produits
import requests
import json
from .models import Produits






def add_product(app, barcode):
    with app.app_context():
        existing_product = Produits.query.filter_by(id=barcode).first()

        if existing_product is None:
            api_url = f'https://world.openfoodfacts.org/api/v2/product/{barcode}.json'
            response = requests.get(api_url)

            if response.status_code == 200:
                product_data = response.json()
                categories=product_data.get('product',{}).get('categories',{})
                # Extraction des informations nutritionnelles
                nutriments = product_data.get('product', {}).get('nutriments', {})

                # Extraction des valeurs nutritionnelles pertinentes
                proteines = nutriments.get('proteins', 'N/A')
                fibres = float(nutriments.get('fiber', '0.0')) if isinstance(nutriments.get('fiber'), (int, float, str)) and str(nutriments.get('fiber')).replace('.', '').isdigit() else None
                energie = float(nutriments.get('energy-kcal_100g', '0.0')) if isinstance(nutriments.get('energy-kcal_100g'), (int, float, str)) and str(nutriments.get('energy-kcal_100g')).replace('.', '').isdigit() else None
                sugars = float(nutriments.get('sugars', '0.0')) if isinstance(nutriments.get('sugars'), (int, float, str)) and str(nutriments.get('sugars')).replace('.', '').isdigit() else None
                sodium = float(nutriments.get('sodium', '0.0')) if isinstance(nutriments.get('sodium'), (int, float, str)) and str(nutriments.get('sodium')).replace('.', '').isdigit() else None
                # Extraction du nom du produit
                product_name = product_data.get('product', {}).get('product_name', 'N/A')

                # Extraction des composants pertinents (par exemple, sodium, eau, etc.)
                relevant_components = []
                for ingredient in product_data.get('product', {}).get('ingredients', []):
                    ingredient_name = ingredient.get('text', 'N/A').lower()  # Convertir en minuscules pour la comparaison
                    relevant_components.append(ingredient_name)

                # Extraction de l'URL de l'image
                image_url = product_data.get('product', {}).get('image_url', 'N/A')

                # Affichage des détails du produit dans la console
                print(f"Nom du produit : {product_name}")
                print("Composants pertinents :")
                components_string = ', '.join(relevant_components)
                print(f"  - {components_string}")
                print(f"URL de l'image : {image_url}")

                # Sauvegarde dans la base de données
                new_product = Produits(
                    id=barcode,
                    name=product_name,
                    categories=categories,
                    components=components_string,
                    proteines=proteines,
                    fibres=fibres,
                    energie=energie,
                    sugars=sugars,
                    sodium=sodium,
                    image_url=image_url
                )

                db.session.add(new_product)
                db.session.commit()



def delete_product(app, barcode):

    with app.app_context():
        existing_product = Produits.query.filter_by(id=barcode).first()
        print(existing_product)
        if existing_product is not None:
            db.session.delete(existing_product)
            db.session.commit()
            print('done')

        else : print('no')

def signaler_produit(app , barcode , nom_poduit , signaleur , cause , wilaya):
    from .models import signalements
    with app.app_context():
        existing_signal = signalements.query.filter_by(signaleur=signaleur , idproduit=barcode ).first()
        if existing_signal is None : 
            new_signalement=signalements(signaleur=signaleur,idproduit = barcode, nom_poduit=nom_poduit , cause = cause, wilaya=wilaya)
            db.session.add(new_signalement)
            db.session.commit()
            db.session.close()


 


