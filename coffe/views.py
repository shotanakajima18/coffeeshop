from flask import request, redirect, url_for, render_template, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField,FileField
from wtforms.validators import InputRequired, Email, Length, NumberRange
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from coffe import app, db
from coffe.models import User, Drink, Foods, Perchase_drink, Perchase_food
from urllib.request import Request, urlopen
import json
import base64
import os

app.config["IMAGE_UPLOADS"] = 'coffe/static/images'

bootstrap=Bootstrap(app)
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view=='login'

class LoginForm(FlaskForm):
    screen_name = StringField('username', validators=[InputRequired(), Length(min=1, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    screen_name = StringField('screen_name', validators=[InputRequired(), Length(min=1, max=15)])
    tel = StringField('tel', validators=[InputRequired(), Length(min=1, max=11)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=80)])

class DrinkForm(FlaskForm):
    
    flavar=StringField('flavar', validators=[InputRequired(), Length(min=1, max=20)])
    price = IntegerField('price', validators=[InputRequired(), NumberRange(min=0, max=100)])
    picture = FileField('picture', validators=[InputRequired()])

class FoodForm(FlaskForm):
    name =StringField('name', validators=[InputRequired(), Length(min=1, max=20)])
    quantity = IntegerField('quantity', validators=[InputRequired(), NumberRange(min=0, max=100)])
    price = IntegerField('price', validators=[InputRequired(), NumberRange(min=0, max=100)])
    picture = FileField('picture', validators=[InputRequired()])
    

class Perchase_drinkForm(FlaskForm):
    quantity = IntegerField('quantity', validators=[InputRequired(), NumberRange(min=0, max=100)])
    drinks_sizes = [(-1, 'Small'), (0, 'Medium'), (1, 'Large')]
    size = SelectField('size', choices = drinks_sizes)
    drink_tem = [('h', 'Hot'), ('c', 'Cold')]
    tem = SelectField('tem', choices = drink_tem)

class Perchase_foodForm(FlaskForm):
    quantity = IntegerField('quantity', validators=[InputRequired(), NumberRange(min=0, max=100)])
    
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/home', )
def home():
    return render_template('index.html')

@app.route('/')
def home1():
    return redirect('/home')

@app.route('/drink_menu') #display
@login_required
def drink_menu():
    drinks=Drink.query.order_by(Drink.id.desc()).all()
    
    return render_template('drink.html', drinks=drinks)


@app.route('/food_menu') #display
@login_required
def food_menu():
    foods =Foods.query.order_by(Foods.id.desc()).all()
    
    return render_template('food.html', foods=foods)




@app.route('/admin_drink', methods=['GET', 'POST'])
@login_required
def admin_drinks():
    form =DrinkForm()
    if request.method =='POST':
        # print('qqqqq')
        if form.validate_on_submit():
            
            
            f = request.form['flavar']
            p = request.form['price']
            pic = request.files['picture']
            pic_name=pic.filename 
            new_drink = Drink (
                                flavar = f,
                                price = p,
                                picture=pic_name
                                )
            print(new_drink)
            
            pic.save(os.path.join(app.config["IMAGE_UPLOADS"], pic.filename))

            db.session.add(new_drink)
            db.session.commit()
            flash('created new drink ')
            return redirect('/admin_drink')
    return render_template('/admin/drink.html', form=form)

@app.route('/admin_food', methods=['GET', 'POST'])
@login_required
def admin_foods():
    form =FoodForm()
    if request.method =='POST':
        # print('qqqqq')
        if form.validate_on_submit():
            n = request.form['name']
            p = request.form['price']
            q= request.form['quantity']
            pic_food= request.files['picture']
            pic_name=pic_food.filename
            new_food = Foods (
                                name = n,
                                price = p,
                                quantity=q,
                                picture=pic_name)
            print(new_food)
            
            pic_food.save(os.path.join(app.config["IMAGE_UPLOADS"], pic_food.filename))

            db.session.add(new_food)
            db.session.commit()
            flash('created new food ')
            return redirect('/admin_food')
    return render_template('/admin/foods.html', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(screen_name=form.screen_name.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    if user.admin:
                        flash('Welcome admin!')
                        return redirect('/home')
                    else:
                        flash('Welcome user!')
                        return redirect('/home')
                    
                flash('Invalid Password')
                return redirect('/login')
            flash('Invalid screen_name or password')
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(screen_name=form.screen_name.data,
                        email=form.email.data,
                        password=hashed_password,
                        tel=form.tel.data
                        )
        db.session.add(new_user)
        db.session.commit()
        flash('New User was successfully created')
        return redirect('/login')
    
    return render_template('register.html', form=form)

@app.route('/buy_drink/<int:drink_id>' , methods=['GET', 'POST'])
@login_required
def show_drink(drink_id):
    form = Perchase_drinkForm()
    id_drink =Drink.query.get(drink_id)
    
    if request.method=='POST':
        if form.validate_on_submit():
            total = (int(form.size.data)+id_drink.price)*form.quantity.data
            perchase_drink = Perchase_drink (
                user_id=current_user.id,
                drink_id=id_drink.id,
                quantity = form.quantity.data,
                price=total,
                tem=form.tem.data,
                size=form.size.data
            )
            
            db.session.add(perchase_drink)
            db.session.commit()
            flash('Successful purchase drink')
            return redirect('/home')
    
    return render_template('/perchase/drink.html', form = form, drink=id_drink)


@app.route('/admin/edit_drink/<int:drink_id>', methods=['GET', 'POST'])
@login_required
def edit_drink(drink_id):
    drink = Drink.query.get(drink_id)

    if request.method == 'POST':
        
        drink.flavar=request.form['flavar']
        drink.price=request.form['price']
        db.session.commit()
        flash('drink was succesaly Update')
        return redirect('/home')
    
        
    return render_template('admin/edit_drink.html',drink=drink)


@app.route('/admin/delete_drink/<int:drink_id>')
@login_required
def delete_drink(drink_id):
    drink=Drink.query.get(drink_id)
    db.session.delete(drink)
    db.session.commit()
    flash('drink was successfuly delete ')
    return redirect('/home')

    


@app.route('/buy_food/<int:food_id>' , methods=['GET', 'POST'])
@login_required
def show_food(food_id):
    form = Perchase_foodForm()
    id_food =Foods.query.get(food_id)
    
    if request.method=='POST':
        if form.validate_on_submit():
            perchase_food = Perchase_food (
                user_id=current_user.id,
                food_id=id_food.id,
                quantity = form.quantity.data,
                price=id_food.price
            )
            
            db.session.add(perchase_food)
            db.session.commit()
            
            id_food.quantity = id_food.quantity -  form.quantity.data
            db.session.commit()


            flash('Successful purchase food')
            return redirect('/home')
    
    return render_template('/perchase/food.html', form = form, food=id_food)

@app.route('/admin/edit_food/<int:food_id>', methods=['POST', 'GET'])
@login_required
def edit_food(food_id):
    food=Foods.query.get(food_id)
    if request.method=='POST':
        food.name = request.form['name']
        food.price= request.form['price']
        food.quantity = request.form['quantity']

        db.session.commit()
        flash('Food was successufuly Update')
        return redirect('/home')

    return render_template('/admin/edit_food.html', food=food)



@app.route('/user/me/')
@login_required
def show_me():
    return render_template('/user/show.html', user = current_user)

@app.route('/user/me/edit', methods=['POST', 'GET'])
@login_required
def edit_me():
    if request.method == 'POST':
        current_user.screen_name =request.form['screen_name']
        current_user.email= request.form['email']
        current_user.tel = request.form['tel']
        db.session.commit()
        flash('Successfully edited your information')
        return redirect(url_for('show_me'))
    return render_template('/user/edit.html', user = current_user)





@app.route('/logout')
@login_required
def logout():
    
    return redirect('/login')

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')










    