from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField ,SelectField,IntegerField
from wtforms.validators import DataRequired , Length , Email , equal_to

class registrationForm(FlaskForm):
    wilaya_choices = [
        ('Adrar', 'Adrar'),
        ('Chlef', 'Chlef'),
        ('Laghouat', 'Laghouat'),
        ('Oum El Bouaghi', 'Oum El Bouaghi'),
        ('Batna', 'Batna'),
        ('Béjaïa', 'Béjaïa'),
        ('Biskra', 'Biskra'),
        ('Béchar', 'Béchar'),
        ('Blida', 'Blida'),
        ('Bouira', 'Bouira'),
        ('Tamanrasset', 'Tamanrasset'),
        ('Tébessa', 'Tébessa'),
        ('Tlemcen', 'Tlemcen'),
        ('Tiaret', 'Tiaret'),
        ('Tizi Ouzou', 'Tizi Ouzou'),
        ('Alger', 'Alger'),
        ('Djelfa', 'Djelfa'),
        ('Jijel', 'Jijel'),
        ('Sétif', 'Sétif'),
        ('Saïda', 'Saïda'),
        ('Skikda', 'Skikda'),
        ('Sidi Bel Abbès', 'Sidi Bel Abbès'),
        ('Annaba', 'Annaba'),
        ('Guelma', 'Guelma'),
        ('Constantine', 'Constantine'),
        ('Médéa', 'Médéa'),
        ('Mostaganem', 'Mostaganem'),
        ('M\'Sila', 'M\'Sila'),
        ('Mascara', 'Mascara'),
        ('Ouargla', 'Ouargla'),
        ('Oran', 'Oran'),
        ('El Bayadh', 'El Bayadh'),
        ('Illizi', 'Illizi'),
        ('Bordj Bou Arreridj', 'Bordj Bou Arreridj'),
        ('Boumerdès', 'Boumerdès'),
        ('El Tarf', 'El Tarf'),
        ('Tindouf', 'Tindouf'),
        ('Tissemsilt', 'Tissemsilt'),
        ('El Oued', 'El Oued'),
        ('Khenchela', 'Khenchela'),
        ('Souk Ahras', 'Souk Ahras'),
        ('Tipaza', 'Tipaza'),
        ('Mila', 'Mila'),
        ('Aïn Defla', 'Aïn Defla'),
        ('Naâma', 'Naâma'),
        ('Aïn Témouchent', 'Aïn Témouchent'),
        ('Ghardaïa', 'Ghardaïa'),
        ('Relizane', 'Relizane')
    ]
    nom = StringField ('nom' , validators=[DataRequired(), Length(min=2,max = 25)])
    prenom = StringField ('prenom' , validators=[DataRequired(), Length(min=2,max = 25)])
    username= StringField ('nom utilisateur' , validators=[DataRequired(), Length(min=2,max = 25)])
    wilaya = SelectField('Wilaya', choices=wilaya_choices, validators=[DataRequired()])
    email = StringField('email' , validators=[DataRequired()])
    password = PasswordField('password' , validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password' , validators=[DataRequired() ,equal_to('password') ])
    submit = SubmitField('Signe Up')

class loginForm(FlaskForm):
    email = StringField('email' , validators=[DataRequired(),Email()])
    password = PasswordField('password' , validators=[DataRequired()])
    remember= BooleanField('Remember Me')
    submit = SubmitField('Login')

class Addproduct(FlaskForm):
    barcode = StringField('barcode')
    submit = SubmitField('add_prod')

class DeleteProductForm(FlaskForm):
    barcode = StringField('barcode')
    delete = SubmitField('Delete')


class SignalerProduit(FlaskForm):
    cause = StringField('la cause du signalement' , validators=[DataRequired()])
    submit = SubmitField('Signaler')

class DeleteUserForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    delete = SubmitField('Delete User')