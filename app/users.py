import decimal
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

class UpdateProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update Information')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')
        
class CurrencyField(DecimalField):
    """
    Very similar to WTForms DecimalField, except with the option of rounding
    the data always.
    https://stackoverflow.com/questions/27781926/decimal-field-rounding-in-wtforms/35359450#35359450
    """
    def __init__(self, label=None, validators=None, places=2, rounding=None,
                 round_always=True, **kwargs):
        super(CurrencyField, self).__init__(
            label=label, validators=validators, places=places, rounding=
            rounding, **kwargs)
        self.round_always = round_always

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = decimal.Decimal(valuelist[0])
                if self.round_always and hasattr(self.data, 'quantize'):
                    exp = decimal.Decimal('.1') ** self.places
                    if self.rounding is None:
                        quantized = self.data.quantize(exp)
                    else:
                        quantized = self.data.quantize(
                            exp, rounding=self.rounding)
                    self.data = quantized
            except (decimal.InvalidOperation, ValueError):
                self.data = None
                raise ValueError(self.gettext('Not a valid decimal value')) 

class AddWithdrawFundsForm(FlaskForm):
    CURRENCY_FIELD_LABEL = 'Amount (automatically rounds to the nearest cent)'

    def __init__(self, max_value=float('inf'), *args, **kwargs):
        super(AddWithdrawFundsForm, self).__init__(*args, **kwargs)
        self.amount.validators = [DataRequired(), NumberRange(0, max_value)]

    amount = CurrencyField(CURRENCY_FIELD_LABEL)
    submit = SubmitField('Submit')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data, 
                         form.address.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/update/<int:uid>', methods=['GET', 'POST'])
def update(uid):
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if User.update(uid,
                        form.email.data,
                        form.firstname.data,
                        form.lastname.data, 
                        form.address.data):
            return redirect(url_for('users.homepage'))
    return render_template('updateProfile.html', title="Update Profile", form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/homepage')
def homepage():
    return render_template('homepage.html')

@bp.route('/profile/<int:uid>')
def profile(uid):
    return render_template('profile.html')

@bp.route('/balance/<int:uid>')
def balance(uid):
    return render_template('balance.html')

@bp.route('/balance/<int:uid>/add', methods=['GET', 'POST'])
def add_funds(uid):
    form = AddWithdrawFundsForm()
    if form.validate_on_submit():
        if User.add_funds(uid,
                        form.amount.data):
            return redirect(url_for('users.balance', uid = uid))
    return render_template('addFunds.html', title = "Add Funds", form = form)

@bp.route('/balance/<int:uid>/withdraw', methods=['GET', 'POST'])
def withdraw_funds(uid):
    balance = User.get_balance(uid)
    form = AddWithdrawFundsForm(max_value = balance)
    if form.validate_on_submit():
        if User.withdraw_funds(uid,
                        form.amount.data):
            return redirect(url_for('users.balance', uid = uid))
    return render_template('withdrawFunds.html', title = "Withdraw Funds", form = form)
