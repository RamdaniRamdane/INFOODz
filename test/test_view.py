# tests/test_views.py
from website import create_app, db
from website.models import User, Produits , signalements
from website import add_product, delete_product, signaler_produit
import pytest

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True  
    app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://admin:rey667.@localhost/reytest2"
    with app.app_context():
        db.create_all()
        yield app
        db.session.rollback()
        db.session.remove()

def test_add_product(app):
    barcode = '6130760000102' 
    add_product(app, barcode)
    product = Produits.query.filter_by(id=barcode).first()
    assert product is not None

def test_delete_product(app):
    barcode = '6130760000102'
    add_product(app, barcode)
    delete_product(app, barcode)
    product = Produits.query.filter_by(id=barcode).first()
    assert product is None

def test_signaler_produit(app):
    barcode = '6130760000102'
    add_product(app, barcode)
    user_id = 1  
    signaler_produit(app, barcode, "Nom du produit", user_id, "Cause du signalement", "Wilaya")
    signalement = signalements.query.filter_by(signaleur=user_id, idproduit=barcode).first()
    assert signalement is not None
