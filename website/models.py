from . import db 

class User(db.Model):
    
    #tablename
    __tablename__ = 'User'

    #columns
    id=db.Column(db.Integer , primary_key=True , autoincrement=True)
    nom=db.Column('name',db.String(50) , nullable = False)
    prenom=db.Column('prenom' ,db.String(50) , nullable=False)
    username=db.Column('username' , db.String(50)  , unique=True , nullable= False)
    wilaya=db.Column('wilaya',db.String(255), nullable=False)
    email=db.Column(db.String(100),unique=True , nullable =False)
    password=db.Column(db.String(100),nullable = False)
    @staticmethod
    def delete_user(user_id):
        user_to_delete = User.query.get(user_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()

            
class Produits(db.Model):

    #table name
    __tablename__ = 'produits'

    #columns
    id=db.Column(db.String(500) , primary_key=True )
    name = db.Column(db.String(5000) , unique=True , nullable=False)
    categories=db.Column(db.String(1000))
    components = db.Column(db.String(5000))
    proteines=db.Column(db.Float)
    fibres=db.Column(db.Float)
    energie=db.Column(db.Float)
    sugars=db.Column(db.Float)
    sodium=db.Column(db.Float)
    image_url=db.Column(db.String(1000))
    def update_attributes(self, new_attributes):
        # Mettez à jour les attributs avec les nouvelles valeurs
        for key, value in new_attributes.items():
            setattr(self, key, value)
        db.session.commit()

class signalements(db.Model):
    __tablename__ = 'signalements'

    id= db.Column(db.Integer,primary_key=True , autoincrement = True)
    signaleur=db.Column(db.Integer)
    idproduit=db.Column(db.String(500))
    nom_poduit=db.Column(db.String(100))
    cause=db.Column(db.String(5000), nullable=False)
    wilaya=db.Column('wilaya',db.String(255), nullable=False)



