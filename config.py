from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# initializing itself

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://thlivnat:1234@localhost:5430/FreestyleAcademySMS"

db.init_app(app)


# --------------------------------------------------------------------------


class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_email = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

# --------------------------------------------------------------------------


class Employee(db.Model):
    __tablename__ = 'Employees'

    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    job = db.Column(db.String)
    position = db.Column
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.class_id'))
    
    profile_image_id = db.Column(db.Integer, db.ForeignKey('Employee_images.image_id'))
    profile_image = db.relationship('EmployeeProfileImage', foreign_keys=[profile_image_id])
    
    # enrollments = db.relationship('Enrollment', back_populates='enrolled_employee')
    # ^ caused mapping errors in the database (idk wtf was wrong but it works now)
# --------------------------------------------------------------------------


class Student(db.Model):
    __tablename__ = 'Students'

    student_id = db.Column(db.Integer, unique=True, primary_key=True)
    student_email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    grade = db.Column(db.Integer)
    age = db.Column(db.Integer)
    
    
    profile_image_id = db.Column(db.Integer, db.ForeignKey('Student_images.image_id'))
    profile_image = db.relationship('StudentProfileImage', foreign_keys=[profile_image_id])
    
    
    enrollments = db.relationship('Enrollment', back_populates='enrolled_student')
    
    
# --------------------------------------------------------------------------
    
    
class Enrollment(db.Model):
    __tablename__ = 'Enrollments'

    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Students.student_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('Classes.class_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('Employees.employee_id'))
    period = db.Column(db.Integer) 
    
    enrolled_class = db.relationship('Class', back_populates='enrollments')    
    enrolled_student = db.relationship('Student', back_populates='enrollments')
    
    # enrolled_teacher = db.relationship('Employee', back_populates='enrollments')
    # ^ caused mapping errors in the database (idk wtf was wrong but it works now)
   
    

# --------------------------------------------------------------------------


class Class(db.Model):
    __tablename__ = 'Classes'

    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String)
    room_number = db.Column(db.Integer)
    period = db.Column(db.Integer)
    # teacher_id = db.Column(db.Integer, db.ForeignKey('Employees.employee_id'))

    
    enrollments = db.relationship('Enrollment', back_populates='enrolled_class')

# --------------------------------------------------------------------------   


class StudentProfileImage(db.Model):
    __tablename__ = 'Student_images'

    image_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Students.student_id'))
    image_path = db.Column(db.String)
    # image path is stored as a string  
    
    
    

# --------------------------------------------------------------------------   


class EmployeeProfileImage(db.Model):
    __tablename__ = 'Employee_images'

    image_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('Employees.employee_id'))
    image_path = db.Column(db.String)
    # image path is stored as a string  
    


with app.app_context():
    db.create_all()