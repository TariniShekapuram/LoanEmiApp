# save this as app.py
from os import name
from flask import Flask,request, render_template,redirect
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
import pickle
import numpy as np

# from flask_login import UserMixin,LoginManager, login_manager,login_user,login_required,logout_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Length,Email
from werkzeug.security import generate_password_hash,check_password_hash


app = Flask(__name__)
bootstrap=Bootstrap(app)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
# app.config['SECRET_KEY']="myloanapp"

# db=SQLAlchemy(app)
# login_manager=LoginManager()
# login_manager.init_app(app)
# login_manager.login_view='login'

# #usertable
# class User(db.Model,UserMixin):
#     id=db.Column(db.Integer,primary_key=True)
#     username=db.Column(db.String(15),nullable=False,unique=True)
#     password=db.Column(db.String(80),nullable=False) 
#     email=db.Column(db.String(50),unique=True) 

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class LoginForm(FlaskForm):
#     username=StringField('UserName',validators=[InputRequired(),Length(min=4,max=15)])
#     password=PasswordField('Password',validators=[InputRequired(),Length(min=8,max=80)])
#     remember=BooleanField('Remember Me')

# class RegisterForm(FlaskForm):
#     email=StringField('Email',validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
#     username=StringField('UserName',validators=[InputRequired(),Length(min=4,max=15)])
#     password=PasswordField('Password',validators=[InputRequired(),Length(min=8,max=80)])

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('prediction.html')

# @app.route('/registration',methods=['GET','POST'])
# def register():
#     form=RegisterForm()
#     if form.validate_on_submit():
#         hashed_password=generate_password_hash(form.password.data,method='sha256')
#         new_user=User(username=form.username.data,email=form.email.data,password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return render_template("index.html")
#         #return '<h1>'+form.username.data+" "+form.password.data+" "+form.email.data+"</h1>"
#     return render_template("registration.html",form=form)


# @app.route('/login',methods=['GET','POST'])
# def login():
#     form=LoginForm()
#     if form.validate_on_submit():
#         user=User.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password,form.password.data):
#                 login_user(user,remember=form.remember.data)
#                 return render_template("index.html")
#         text="Please SignUp First"
#         return render_template('login.html',loan_text="{}".format(text),form=form)
#        # return '<h1>'+form.username.data+" "+form.password.data+"</h1>"
#     return render_template('login.html',form=form)

@app.route('/emi.html')
# @login_required
def emi():
    return render_template("emi.html")

@app.route('/predict', methods=['GET', 'POST'])
# @login_required
def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        if (gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif(dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(area=="Semiurban"):
            semiurban=1
            urban=0
        elif(area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0


        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[credit, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])

        # print(prediction)

        if(prediction=="N"):
            prediction="Not Approved"
        else:
            prediction="Approved"


        return render_template("prediction.html", prediction_text="Your Loan status is {}".format(prediction))
    else:
        return render_template("prediction.html")

# @app.route('/logout',methods=['GET','POST'])
# def logout():
#     form=LoginForm()
#     if form.validate_on_submit():
#         user=User.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password,form.password.data):
#                 login_user(user,remember=form.remember.data)
#                 return render_template("index.html")
#         return '<h1>Invalid username or password</h1>'
#        # return '<h1>'+form.username.data+" "+form.password.data+"</h1>"
#     return render_template('login.html',form=form)

# def logout():
#     form=LoginForm()
#     logout_user()
#     return render_template("login.html",form=form)

if __name__ == "__main__":
    app.run(debug=True)