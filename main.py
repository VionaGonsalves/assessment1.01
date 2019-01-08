from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Connecting to database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:viona@localhost/assessment1.0'
app.config['SECRET_KEY'] = 'vionag'

db = SQLAlchemy(app)


# Creating Student entity
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # Foreign Key
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    created_on = db.Column(db.DateTime(), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(), server_default=db.func.now())
    classes = db.relationship('Classes', foreign_keys='Classes.class_leader')

    def __init__(self, name, class_id):
        self.name = name
        self.class_id = class_id


# Creating Class entity
class Classes(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    # Foreign Key
    class_leader = db.Column(db.Integer, db.ForeignKey('student.id'))
    created_on = db.Column(db.DateTime(), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(), server_default=db.func.now())
    student = db.relationship('Student', foreign_keys='Student.class_id')

    def __init__(self, class_name):
        self.class_name = class_name


# Displaying Student Details
@app.route('/', methods=['GET', 'POST'])
def show_all():
    db.create_all()
    return render_template('student_table.html', students=Student.query.all())


# Adding a new student record
@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['class_id'] or not request.form['class_leader']:
            flash('Please enter all fields', 'error')
        else:
            class_leader = request.form['class_leader']
            if class_leader == 'Yes':
                student = Student(request.form['name'], request.form['class_id'])
                class_details = Classes.query.filter_by(class_id=request.form['class_id']).first()

                db.session.add(student)
                db.session.commit()

                class_details.class_leader = student.id
                class_details.updated_on = db.func.now()
                db.session.add(class_details)
                db.session.commit()
            else:
                student = Student(request.form['name'], request.form['class_id'])
                db.session.add(student)
                db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('new_record.html', classes=Classes.query.all())


# Adding a new class record
@app.route('/new_class_record', methods=['GET', 'POST'])
def new_class_record():
    if request.method == 'POST':
        if not request.form['class_name']:
            flash('Please enter all details', 'error')
        else:
            class_info = Classes(request.form['class_name'])
            db.session.add(class_info)
            db.session.commit()
            return redirect(url_for('class_table'))
    return render_template('new_class.html', classes=Classes.query.all())


# Displaying class details
@app.route('/class_table', methods=['GET', 'POST'])
def class_table():
    return render_template('class_table.html', classes=Classes.query.all())


# Passing student details to be updated
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form.get('id')
        student = Student.query.filter_by(id=id).first()
        return render_template('update.html', student=student)


# Updating student record
@app.route('/update_rec', methods=['POST'])
def update_rec():
    if not request.form['name'] or not request.form['class_id']:
        flash('Please enter all the fields', 'error')
    else:
        class_leader = request.form['class_leader']
        if class_leader == 'Yes':
            id = request.form.get('id')
            student = Student.query.filter_by(id=id).first()
            class_details = Classes.query.filter_by(class_id=request.form['class_id']).first()
            print(student.name)
            student.name = request.form['name']
            student.class_id = request.form['class_id']
            student.updated_on = db.func.now()

            class_details.class_leader = student.id
            class_details.updated_on = student.updated_on
            print(class_details.class_leader)
            db.session.commit()

        else:
            id = request.form.get('id')
            student = Student.query.filter_by(id=id).first()
            student.name = request.form['name']
            student.class_id = request.form['class_id']
            student.updated_on = db.func.now()

            db.session.commit()

    return render_template('student_table.html', students=Student.query.all(), classes=Classes.query.all())


# Deleting student record
@app.route('/delete_student', methods=['POST'])
def delete_student():
    if request.method == 'POST':
        student_id = request.form.get('id')
        student = Student.query.filter_by(id=student_id).first()
    try:
        db.session.delete(student)
        db.session.commit()
        return render_template('student_table.html', students=Student.query.all())
    except IntegrityError:
        flash('The student you are trying to delete is the current class leader.'
              'Please appoint a new class leader')
        return render_template('student_table.html', students=Student.query.all())


if __name__ == '__main__':
    db.create_all()
    app.run(debug='True')

