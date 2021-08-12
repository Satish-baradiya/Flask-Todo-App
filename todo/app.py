from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean())


@app.route('/')
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html',todo_list=todo_list)


@app.route('/add',methods=['POST','GET'])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))






if __name__ == "__main__":
    app.run(debug=True)