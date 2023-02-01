from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, redirect, render_template, request, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
app = Flask(__name__)
app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My Flask App"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = "user" + str(id)
        self.password = self.username + "_secret"

    def __str__(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return redirect('/login')

    login_user(registered_user)
    return redirect('/home')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run()