""" CRUD Operations"""
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import uuid

# Connecting to database
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:viona@localhost/assessment1.0'
APP.config['SECRET_KEY'] = 'vionag'

DB = SQLAlchemy(APP)


# Creating Student entity
class Student(DB.Model): # pylint: disable=too-few-public-methods
    """Creating Student Entity"""
    student_id = DB.Column('id', DB.String(100), primary_key=True)
    name = DB.Column(DB.String(100))
    # Foreign Key
    class_id = DB.Column(DB.String(100), DB.ForeignKey('classes.id'))
    created_on = DB.Column(DB.DateTime(), server_default=DB.func.now())
    updated_on = DB.Column(DB.DateTime(), server_default=DB.func.now())
    classes = DB.relationship('Classes', foreign_keys='Classes.class_leader')

    def __init__(self, student_id, name, class_id):
        self.student_id = student_id
        self.name = name
        self.class_id = class_id


# Creating Class entity
class Classes(DB.Model): # pylint: disable=too-few-public-methods
    """Creating Class Entity"""
    class_id = DB.Column('id', DB.String(100), primary_key=True)
    class_name = DB.Column(DB.String(100))
    # Foreign Key
    class_leader = DB.Column(DB.String(100), DB.ForeignKey('student.id'))
    created_on = DB.Column(DB.DateTime(), server_default=DB.func.now())
    updated_on = DB.Column(DB.DateTime(), server_default=DB.func.now())
    student = DB.relationship('Student', foreign_keys='Student.class_id')

    def __init__(self, class_id, class_name):
        self.class_id = class_id
        self.class_name = class_name


# Displaying Student Details
@APP.route('/', methods=['GET', 'POST'])
def show_all():
    """Displaying Student Details"""
    DB.create_all()
    return render_template('student_table.html', students=Student.query.all())


# Adding a new student record
@APP.route('/new_student', methods=['GET', 'POST'])
def new_student():
    """Adding new student record"""
    if request.method == 'POST':
        if not request.form['name'] or\
                not request.form['class_id'] or not request.form['class_leader']:
            flash('Please enter all fields', 'error')
        else:
            class_leader = request.form['class_leader']
            if class_leader == 'Yes':
                uid_id = uuid.uuid1()
                student = Student(uid_id.int, request.form['name'], request.form['class_id'])
                class_details = Classes.query.filter_by(class_id=request.form['class_id']).first()

                DB.session.add(student)
                DB.session.commit()

                class_details.class_leader = student.student_id
                class_details.updated_on = DB.func.now()
                DB.session.add(class_details)
                DB.session.commit()
                flash('Student added successfully')
            else:
                uid_id = uuid.uuid1()
                student = Student(uid_id.int, request.form['name'], request.form['class_id'])
                DB.session.add(student)
                DB.session.commit()
                flash('Student added successfully')
            return redirect(url_for('show_all'))
    return render_template('new_record.html', classes=Classes.query.all())


# Adding a new class record
@APP.route('/new_class_record', methods=['GET', 'POST'])
def new_class_record():
    """Adding a new class record"""
    if request.method == 'POST':
        if not request.form['class_name']:
            flash('Please enter all details', 'error')
        else:
            uid_id = uuid.uuid1()
            class_info = Classes(uid_id.int, request.form['class_name'])
            DB.session.add(class_info)
            DB.session.commit()
            return redirect(url_for('class_table'))
    return render_template('new_class.html', classes=Classes.query.all())


# Displaying class details
@APP.route('/class_table', methods=['GET', 'POST'])
def class_table():
    """Displaying class details"""
    return render_template('class_table.html', classes=Classes.query.all())


# Passing student details to be updated
@APP.route('/update', methods=['POST'])
def update():
    """Passing student details to be updated"""
    if request.method == 'POST':
        student_id = request.form.get('id')
        student = Student.query.filter_by(student_id=student_id).first()
        return render_template('update.html', student=student)
    return redirect(url_for(show_all))


# Updating student record
@APP.route('/update_rec', methods=['POST'])
def update_rec():
    """Updating student record"""
    if not request.form['name'] or not request.form['class_id']:
        flash('Please enter all the fields', 'error')
    else:
        class_leader = request.form['class_leader']
        if class_leader == 'Yes':
            student_id = request.form.get('id')
            student = Student.query.filter_by(student_id=student_id).first()
            class_details = Classes.query.filter_by(class_id=request.form['class_id']).first()
            print(student.name)
            student.name = request.form['name']
            student.class_id = request.form['class_id']
            student.updated_on = DB.func.now()

            class_details.class_leader = student.student_id
            class_details.updated_on = student.updated_on
            print(class_details.class_leader)
            DB.session.commit()
            flash('Student details updated successfully')
        else:
            student_id = request.form.get('id')
            student = Student.query.filter_by(student_id=student_id).first()
            student.name = request.form['name']
            student.class_id = request.form['class_id']
            student.updated_on = DB.func.now()

            DB.session.commit()
            flash('Student details updated successfully')
    return render_template('student_table.html', students=Student.query.all(),
                           classes=Classes.query.all())


# Deleting student record
@APP.route('/delete_student', methods=['POST'])
def delete_student():
    """Deleting student record"""
    if request.method == 'POST':
        student_id = request.form.get('id')
        student = Student.query.filter_by(student_id=student_id).first()
    try:
        DB.session.delete(student)
        DB.session.commit()
        flash('Student Deleted Successfully!')
        return render_template('student_table.html', students=Student.query.all())
    except IntegrityError:
        flash('The student you are trying to delete is the current class leader.'
              'Please appoint a new class leader')
        return render_template('student_table.html', students=Student.query.all())


if __name__ == '__main__':
    DB.create_all()
    APP.run(debug='True')
