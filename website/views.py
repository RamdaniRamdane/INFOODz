from flask import render_template , flash , redirect , url_for ,session , request
from .forms import registrationForm , loginForm , Addproduct , DeleteProductForm , SignalerProduit
from website import bcrypt , add_product , delete_product , signaler_produit

def views(app):
    @app.route("/")
    def home():
        from .models import Produits
        products = Produits.query.all()
        return render_template('home.html',products=products)

    from sqlalchemy import desc

    @app.route("/produits", methods=['GET','POST'])
    def produits():
        from .models import Produits
        delete_form = DeleteProductForm()
        search_term = request.args.get('search', default='')
        sort_by = request.args.get('sort_by', default='id')
        if delete_form.validate_on_submit() and session.get('admin'):
            delete_product(app, delete_form.barcode.data)

        if sort_by not in ['id', 'categories', 'proteines', 'fibres', 'energie', 'sugars', 'sodium']:
            sort_by = 'id'  # Assurez-vous que sort_by est une valeur valide

        # if search_term:
        #     products = Produits.query.filter(Produits.name.ilike(f"%{search_term}%"))
        if search_term:
            pr=Produits.query.filter(Produits.name.ilike(f"{search_term}%"))
            if pr :
                products=Produits.query.filter(Produits.name.ilike(f"{search_term}%"))
            elif pr is not None: 
                products=Produits.query.filter(Produits.name.ilike(f"%{search_term}%"))
        else:
            products = Produits.query

        # Ajoutez la logique de tri ici
        if sort_by == 'id':
            products = products.order_by(Produits.id)
        elif sort_by == 'categories':
            products = products.order_by(Produits.categories)
        elif sort_by == 'proteines':
            products = products.order_by(desc(Produits.proteines))
        elif sort_by == 'fibres':
            products = products.order_by(desc(Produits.fibres))
        elif sort_by == 'energie':
            products = products.order_by(desc(Produits.energie))
        elif sort_by == 'sugars':
            products = products.order_by(desc(Produits.sugars))
        elif sort_by == 'sodium':
            products = products.order_by(desc(Produits.sodium))

        products = products.all()

        return render_template('produits.html', products=products, search_term=search_term, sort_by=sort_by,delete_form=delete_form)




    
    @app.route('/product/info/<int:product_id>')
    def product_info(product_id):
        from .models import Produits
    # Supposons que vous ayez une fonction pour obtenir les informations du produit par son ID
        product = Produits.query.filter_by(id=product_id).first()  # Remplacez ceci par votre fonction
        return render_template('product_info.html', product=product)
    
    
    @app.route('/product/info/<int:product_id>/signaler' , methods=['GET','POST'])
    def signaler(product_id):
        from .models import Produits , User 
        from . import signaler_produit
        signaleur=User.query.filter_by(id=session['id']).first()
        produit=Produits.query.filter_by(id=product_id).first()
        signal_form=SignalerProduit()
        if signal_form.validate_on_submit():
            # signaler_produit(app , barcode , nom_poduit , signaleur , cause , wilaya)
            signaler_produit(app ,product_id ,produit.name , signaleur.id , signal_form.cause.data , signaleur.wilaya)
            return redirect(url_for('product_info', product_id=product_id))
        return render_template('signaler.html' , signal_form=signal_form)



    @app.route('/product/info/<int:product_id>/signalements', methods=['GET'])
    def signale_display(product_id):
        from .models import signalements
        signalements = signalements.query.filter(signalements.idproduit == product_id).all()
        return render_template('signale_display.html' ,signalements=signalements)
    

    @app.route("/alerts/" , methods=['GET'])
    def alerts():
        wilaya = request.args.get('wilaya', 'all')
        from .models import signalements
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
        print("Received wilaya:", wilaya)
        if wilaya == 'all' or wilaya == '':
            # Afficher tous les signalements sans filtre de wilaya
            signalements_filtered = signalements.query.all()
        else:
            # Filtrer les signalements par wilaya
            signalements_filtered = signalements.query.filter_by(wilaya=wilaya).all()

        return render_template('alerts.html', signalements=signalements_filtered, selected_wilaya=wilaya ,wilaya_choices=wilaya_choices)

    
    @app.route("/register" , methods=['GET','POST'])
    def register():
        from . import create_user
        form = registrationForm()
        print(form.validate_on_submit())
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            create_user(app, form.nom.data , form.prenom.data,form.username.data ,form.wilaya.data ,form.email.data ,hashed_password)
            flash(f"Account created successfully for {form.prenom.data}", "success")
            return redirect(url_for('login'))
        # else:
        #     err=form.errors  # Affichez les erreurs dans la console
        return render_template('register.html' , form=form)
    
    @app.route("/login" , methods=["GET","POST"])
    def login():
        from .auth import check_login
        from .models import User
        form = loginForm()
        session['login']=False
        session['id']=0
        session['admin']=False
        if form.validate_on_submit() and check_login(form.email.data , form.password.data) :
            user=User.query.filter_by(email=form.email.data).first()
            session['login']=True
            session['id']=user.id
            if user.username=='admin' :
                session['admin']=True
            print(login , id)
            flash("connected successfully ", "success")
            return redirect(url_for('home'))
        return render_template('login.html' , form=form)
    
    @app.route('/logout')
    def logout():
        session['login'] = False
        session['id']= 0
        session['admin']=False
        return redirect(url_for('home'))
    

    @app.route('/dashboard', methods=["GET", "POST"])
    def dashboard():
        from flask import render_template, request, flash, redirect, url_for
        from .models import Produits, User
        from .forms import Addproduct, DeleteProductForm, DeleteUserForm
        users = User.query.all()
        products = Produits.query.all()

        add_form = Addproduct()
        delete_product_form = DeleteProductForm()
        delete_user_form = DeleteUserForm()

        if request.method == 'POST':
            if add_form.submit.data and add_form.submit():
                add_product(app, add_form.barcode.data)
                flash('Product added successfully!', 'success')
                print('1 s execute')
            elif delete_product_form.delete.data and delete_product_form.validate_on_submit():
                barcode_to_delete = delete_product_form.barcode.data
                delete_product(app, barcode_to_delete)
                flash('Product deleted successfully!', 'success')
                print('2 s execute')
            if delete_user_form.delete():
                user_id_to_delete = delete_user_form.user_id.data
                User.delete_user(user_id_to_delete)
                flash('User deleted successfully!', 'success')

        return render_template(
            'dashboard.html',
            add_form=add_form,
            delete_product_form=delete_product_form,
            delete_user_form=delete_user_form,
            users=users,
            products=products
        )
    




    from werkzeug.utils import secure_filename
    from werkzeug.exceptions import BadRequest
    import os 
    @app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
    def edit_product(product_id):
        from .models import Produits
        # Récupérez le produit à partir de la base de données en fonction de l'ID
        product = Produits.query.get(product_id)

        if request.method == 'POST':
            # Récupérez les nouvelles valeurs depuis le formulaire
            new_attributes = {
                'proteines': request.form.get('proteines'),
                'fibres': request.form.get('fibres'),
                'energie': request.form.get('energie'),
                'sugars': request.form.get('sugars'),
                'sodium': request.form.get('sodium'),
                'categories': request.form.get('categories'), 
                'ingredients': request.form.get('ingredients'),
      
            }
            try:
                new_photo = request.files['new_photo']
                if new_photo and new_photo.filename != "":
                    filename = secure_filename(new_photo.filename)
                    destination_folder = app.config['UPLOADED_PHOTOS_DEST']
                    save_path = os.path.join(destination_folder, filename)
                    new_photo.save(save_path)
                    new_attributes['image_url'] = url_for('static', filename='image/' + filename)
                    print('File saved successfully:', save_path)
                    print('Generated image URL:', new_attributes['image_url'])
            except BadRequest:
                flash('Le type de fichier téléchargé n\'est pas autorisé.', 'error')
# ...

            # Mettez à jour les attributs du produit
            product.update_attributes(new_attributes)

            flash('Attributs mis à jour avec succès!', 'success')
            return redirect(url_for('product_info', product_id=product.id))

        return render_template('edit_product.html', product=product)
    


