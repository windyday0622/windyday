from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import pytz
from form import TaskForm
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.config.from_pyfile("config.py")
# app.config['SECRET_KEY'] = 'f291e9719b3ad45eb0ead363d5df5c0014c337d3668eb71e'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_pyfile("config.py")

db.init_app(app)
migrate.init_app(app, db)
csrf = CSRFProtect(app)
# class Task(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #title = db.Column(db.String(100), nullable=False)
    #contents = db.Column(db.Text, nullable=False)
    #input_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    #due_date = db.Column(db.Date, nullable=False)


@app.route('/')
def index():
    form = TaskForm()
    csrf_token = form.csrf_token._value()
    return render_template('index.html', form=form, csrf_token=csrf_token)
    #if form.validate_on_submit():
    #   new_task = Task(title=form.title.data)
    #   db.session.add(new_task)
    #   db.session.commit()
    #   return redirect(url_for('index'))    
    #return render_template('index.html', form=form)

@app.route('/tasks')
def tasks():
    tasks = tasks.query.all()
    return jsonify(
        [
            {
                'id': task.id, 
                'title': task.title,
                'contents': task.contents,
                'input_date': task.input_date.strftime('%Y-%m-%d'),
                'due_date': task.due_date.strftime('%Y-%m-%d'),
            } 
            for task in tasks
        ]
 )


@app.route('/', methods=['POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        contents = form.contents.data
       # new_task = Task(title=form.title.data, contents=form.contents.data, due_date=form.due_date.data)
       # db.session.add(new_task)
       # db.session.commit()
       # return redirect(url_for('index'))
   # return render_template('index.html', form=form)

        # 한국 시간으로 현재 날짜 설정
        kst = pytz.timezone('Asia/Seoul')
        input_date = datetime.now(kst).date()

        due_date = form.due_date.data

        new_task = Task(title=title, contents=contents, input_date=input_date, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    csrf_token = form.csrf_token._value()
    return render_template('index.html', form=form, csrf_token=csrf_token)


@app.route("/edit/<int:task_id>", methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task) # teak 객체로 form 객체 초기화
    if request.method == 'POST' and form.validate_on_submit():
        task.title = form.title.data
        task.contents = form.contents.data
        task.due_date = form.due_date.data

        db.session.commit()
        return redirect(url_for('index'))
    csrf_token = form.csrf_token._value()
    # form.title.data = task.title
    return render_template('edit_task.html',
                           form=form, 
                           task_id=task_id, 
                           csrf_token=csrf_token,
                           task_title=task.title, 
                           task_contents=task.contents, 
                           task_input_date=task.input_date.strftime('%Y-%m-%d'),
                           task_due_date=task.due_date.strftime('%Y-%m-%d'),
                           )

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)