import os
from flask import Flask, render_template, redirect, url_for, request, make_response, jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'app.db')

app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

    def __init__(self, title):
        self.title = title
        self.complete = False

@app.route('/set-cache/<country>/<capital>')
def set_cache(country, capital):
    cache.set(country, capital)
    return 'Success'

@app.route('/get-cache/<country>')
def get_cache(country):
    capital = cache.get(country)
    return capital

@app.route('/add-bulk-data')
def bulk_data():

    for i in range(1,1000):
        todo = Todo(f'Todo {i}')
        db.session.add(todo)

    db.session.commit()
    return redirect(url_for('home'))
    # return 'Success'

@app.route('/')
@app.route('/<name>')
def home(name=None):
    data = cache.get('all-data')
    if data is None:
        todo_list = Todo.query.all()
        data = []

        for todo in todo_list:
            data.append({
                'id': todo.id,
                'title': todo.title,
                'complete': todo.complete
            })

        cache.set('all-data', data)
        return jsonify(data)
    # return render_template('todo.html',todo_list=todo_list)

    else:
        return jsonify(data)



@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

    # new_todo - 1234
    # session = [1234]


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


# count = 1

# conn = psycopg2.connect(
#     host='localhost',
#     database="flask_project",
#     user="postgres",
#     password="123456")

# cur = conn.cursor()

# @app.route('/get-db')
# def get_db():
#     cur.execute('SELECT version()')

#     # display the PostgreSQL database server version
#     db_version = cur.fetchone()
#     print(db_version)
#     # close the communication with the PostgreSQL
#     cur.close()
#     return 'True'

# (
#     (1, "eat lunch", True),
#     (2, "eat dinner", False)
# )

# [ ]

# todo_list = []

# # class Todo:
# #     def __init__(self, id, title):
# #         self.id = id
# #         self.title = title
# #         self.complete = False


# # todo = Todo(1, "eat lunch")

# # todo[1]

# @app.route('/')
# def root(name=None):
#     my_dict = {
#         "message" : "hello",
#         "status": 202
#     }
#     return make_response(my_dict), 202

# @app.route('/add', methods = ['POST'])
# def add_todo():
#     global count
#     title = request.form['title']
#     todo = Todo(count, title)
#     count += 1

#     todo_list.append(todo)
#     return redirect(url_for('root'))

# @app.route('/update/<int:id>')
# def update(id):
#     for todo in todo_list:
#         if todo.id == id:
#             todo.complete = True
#             break

#     return redirect(url_for('root'))
    


# # def home(name):
# #     return render_template('ind')


#     # return redirect(url_for('root'))

if __name__ == "__main__":
    app.run()


