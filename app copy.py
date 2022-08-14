import os
from flask import Flask, redirect, url_for, render_template, request
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:123456@localhost:5432/postgres_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    complete = db.Column(db.Boolean, nullable=True)

    def __init__(self, title, complete):
        self.title = title
        self.complete = complete


@app.route('/')
@app.route('/<name>')
def home(name=None):
    todo_list = Todo.query.all()
    return render_template('todo.html',todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    # data = {}
    # count = 0
    app.run()

# data = {}
# count = 0

# conn = psycopg2.connect(
#     host=os.getenviron('HOST'),
#     database="beflask",
#     user="postgres",
#     password="123456")

# (1, "Sadman","email","address")

# cur = conn.cursor()

# @app.route('/get-db')
# def get_db():
#     cur.execute('SELECT version()')

#     # display the PostgreSQL database server version
#     db_version = cur.fetchone()
#     print(db_version)
    
# # close the communication with the PostgreSQL
#     cur.close()
#     return 'True'

# class Todo:
#     def __init__(self, id, title):
#         self.id = id
#         self.title = title
#         self.complete = False

# @app.route('/<name>')
# @app.route('/')
# def index(name=None):
#     return render_template('index.html',my_name=name)

# @app.route('/home/<int:value>/<value2>')
# def home(value, value2):
#     return f"Hello {value} , {value2}"
#     # return redirect(url_for('index'))

# @app.route('/new_value', methods=['POST'])
# def new_value():
#     data = request.get_json()
#     print(data)
#     data['body'] = "asdasdasdasdasdas"
#     return data

# @app.route('/new-todo', methods=['POST'])
# def new_todo():
#     title = request.form['title']
#     global count
#     count = count + 1
#     todo = Todo(count, title)
#     data[todo.id] = todo
#     return redirect(url_for('show_todo'))

# @app.route('/show-todo')
# def show_todo():
#     return render_template('todo.html',todo_list=data)

# @app.route('/update/<int:id>')
# def update(id):
#     todo = data[id]
#     todo.complete = True
#     return redirect(url_for('show_todo'))



















# conn = psycopg2.connect(
#     host="localhost",
#     database="dbv4",
#     user="postgres",
#     password="123456")

# cur = conn.cursor()

# @app.route('/get-db')
# def get_db():
#     cur.execute('SELECT version()')

#     # display the PostgreSQL database server version
#     db_version = cur.fetchone()
#     print(db_version)
    
# # close the communication with the PostgreSQL
#     cur.close()
#     return 'True'



# def encode_auth_token(email):
#     try:
#         user = User.query.filter_by(email=email).first()
#         if user:
#             random_string = uuid.uuid4().hex
#             payload = {
#                 'exp': datetime.utcnow() + timedelta(days=0, seconds=1800),
#                 'iat': datetime.utcnow(),
#                 'email': email,
#                 'random': random_string
#             }
#             token = jwt.encode(payload, app.config.get(
#                 'SECRET_KEY'), algorithm='HS256')
#             return token, random_string
#         return False
#     except Exception as e:
#         return e


# def decode_auth_token(auth_token):
#     try:
#         payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
#         return payload
#     except jwt.ExpiredSignatureError:
#         return 'expired'
#     except jwt.InvalidTokenError:
#         return 'invalid'