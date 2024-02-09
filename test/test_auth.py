from website.auth import check_login
from website.models import db, User
from website import create_app, bcrypt

# Définissez le test pour la fonction check_login
def test_check_login():
    # Utiliser la fonction pour créer l'application Flask
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+mariadbconnector://admin:rey667.@localhost/reytest2"
    # Créer toutes les tables dans la base de données
    with app.app_context():
        db.create_all()

        # Créer un utilisateur pour les besoins du test
        hashed_password = bcrypt.generate_password_hash('password').decode("utf-8")
        user = User(
            nom='rey',
            prenom='hey',
            username='adey',
            wilaya='Alger',
            email='testing@example.com',
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        # Appeler la fonction check_login avec les informations valides
        result_valid = check_login('testing@example.com', 'password')

        # Appeler la fonction check_login avec des informations invalides
        result_invalid = check_login('testing@example.com', 'wrong_password')

    # Asserts pour vérifier les résultats
    assert result_valid is True
    assert result_invalid is False
