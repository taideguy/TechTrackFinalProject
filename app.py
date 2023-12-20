from flask import Flask, render_template, request, redirect, url_for, flash, session
from methods import DatabaseHandler
from config import db
from random import randint





app = Flask(__name__, static_url_path='/static')

app.secret_key = 'yas9df#*7ads987fasd89*f07ads9f7as'
# possibly redundant
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://thlivnat:1234@localhost:5430/FreestyleAcademySMS"

db.init_app(app)

db_handler = DatabaseHandler()
# instantiates DatabaseHandler


# landing page
@app.route('/')
def landing_page():
    
    return render_template("landing.html")


# home button
@app.route('/go-home', methods=['GET', 'POST'])
def home_redirect():
    if request.method == 'POST':
        
        return redirect(url_for('inquire_page'))

# admin button
@app.route('/go-admin', methods=['GET', 'POST'])
def admin_redirect():
    if request.method == 'POST':
        
        return redirect(url_for('admin_page'))
    
# login button redirect
@app.route('/go-login', methods=['GET', 'POST'])
def login_redirect():
    if request.method == 'POST':
        
        return redirect(url_for('login_page'))

# signup button redirect
@app.route('/go-signup', methods=['GET', 'POST'])
def signup_redirect():
    if request.method == 'POST':
        
        return redirect(url_for('signup_page')) 

# SIGNUP ------------------------------------------------------------------------


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        
        db_handler.insert_into_users(
            first_name = request.form['first_name'],
            last_name = request.form['last_name'],
            user_email = request.form['email'],
            password = request.form['password'],
            role = request.form['role'])
        
        user_data = db_handler.get_all_data_from_users()
        
        user_email = request.form['email']
        found_user = None
        
        for user in user_data:
            if user.user_email == user_email:
                found_user = user
                break
        # finding the uploaded user_data to draw first_name and user_id 
                
            
        return redirect(url_for('login_page', first_name=found_user.first_name, user_id=found_user.user_id))
        # link 1 passing name and ID to inquire
        
    return render_template("signup.html")

# LOGIN -------------------------------------------------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    

    if request.method == 'POST':
        
        user_data = db_handler.get_all_data_from_users()
        
        inputted_email = request.form['email'].lower()
        inputted_password = request.form['password'].strip()
        found_user = None
        
        for user in user_data:
            if user.user_email.lower() == inputted_email.lower():
                found_user = user
                # defining the user who's attemping login
                break
            # searching for email 
        else:
            flash('Email Not Found', 'email_error')
            return redirect(url_for('login_page'))
        
        for user in user_data:
            if user.password == inputted_password:
                break
            # authenticating password 
        else:
            flash('Incorrect Password', 'password_error')
            return redirect(url_for('login_page'))
                
        # finding the uploaded user_data to draw user_id 
                
            
        return redirect(url_for('inquire_page', first_name=found_user.first_name, user_id=found_user.user_id, found_user=found_user))
        # link 2 passing name and ID to inquire
    
    return render_template("login.html")



# Inquire --------------------------------------------------------------------------


@app.route('/inquire')
def inquire_page():
    
    student_data = db_handler.get_all_data_from_students()
    class_data = db_handler.get_all_data_from_classes()
    employee_data = db_handler.get_all_data_from_employees()
    enrollment_data = db_handler.get_all_data_from_enrollments()
    
    # for the user data header 
    first_name = request.args.get('first_name')
    user_id = request.args.get('user_id')
    
    return render_template("inquire.html", first_name=first_name, user_id=user_id, student_data=student_data, class_data=class_data, employee_data=employee_data, enrollment_data=enrollment_data)
    
    
    
#----------------------- VIEW ALL

@app.route('/view_all_students', methods=['POST'])
def view_all_students():
    if request.method == 'POST':
        
        student_id = int(request.form['student_id'])
        print(f"Selected Student: {student_id} (ID)")
    
        
        return redirect(url_for('student_profile'), student_id=student_id)
    

@app.route('/view_all_employees', methods=['POST'])
def view_all_employees():
    if request.method == 'POST':
        
        return redirect(url_for('inquire_page'))
        
        
@app.route('/view_all_classes', methods=['POST'])
def view_all_classes():
    if request.method == 'POST':
        
        return redirect(url_for('inquire_page'))
        

#----------------------- VIEW SPECIFIC

@app.route('/view_specific_students', methods=['POST'])
def view_specific_students():
    if request.method == 'POST':
        
        return redirect(url_for('inquire_page'))
    

@app.route('/view_specific_employees', methods=['POST'])
def view_specific_employees():
    if request.method == 'POST':
        
        return redirect(url_for('inquire_page'))
    
    
@app.route('/view_specific_classes', methods=['POST'])
def view_specific_classes():
    if request.method == 'POST':
        
        return redirect(url_for('inquire_page'))


# PROFILE --------------------------------------------------------------------------

@app.route('/profile')
def profile_page():
    
    student_data = db_handler.get_all_data_from_students()
    class_data = db_handler.get_all_data_from_classes()
    employee_data = db_handler.get_all_data_from_employees()
    enrollment_data = db_handler.get_all_data_from_enrollments()
    
    
    return render_template("profile.html", student_data=student_data, class_data=class_data, employee_data=employee_data, enrollment_data=enrollment_data, found_student=found_student, found_enrollment_data=found_enrollment_data, found_class_data=found_class_data )
    


#----------------------- STUDENT PROFILE

@app.route('/student_profile', methods=['GET','POST'])
def student_profile():
    if request.method == 'POST':
        
        student_data = db_handler.get_all_data_from_students()
        enrollment_data = db_handler.get_all_data_from_enrollments()
        class_data = db_handler.get_all_data_from_classes()
        
        student_id = int(request.form['student_id'])
        print(f"Selected Student: {student_id} (ID)")
        
        found_student = None
        found_enrollment_data = []
        found_class_data = []
        
        enrollment_found = False
        
        # finding student data
        for student in student_data:
            if student.student_id == student_id:
                found_student = student
                print(f"Student Found: {found_student.first_name} {found_student.last_name}")
        
        # finding enrollment data    
        if found_student:
            for enrollment in enrollment_data:
                if enrollment.student_id == found_student.student_id:
                    found_enrollment_data.append(enrollment)
                    enrollment_found = True
                    print(f"Enrollment Added: {enrollment.enrollment_id} (ID)")
        
        # finding enrolled class data         
        if found_enrollment_data:
            for classe in class_data:
                for enrollment in found_enrollment_data:
                    if classe.class_id == enrollment.class_id:
                        found_class_data.append(classe)
                        print(f"Class Added: {classe.class_name}")
        
        # redirecting if no enrollment data found              
        if enrollment_found is False:
            found_enrollment_data.append("No Enrollments Found")
            found_class_data.append("No Classes Found")
            print(f"No Enrollments Found: {found_student.first_name} {found_student.last_name} ")
            return render_template('profile.html', found_student=found_student, found_enrollment_data=found_enrollment_data, found_class_data=found_class_data)
        
        return render_template('student_profile.html', found_student=found_student, found_enrollment_data=found_enrollment_data, found_class_data=found_class_data, enrollment_found=enrollment_found)
    
    if request.method == 'GET':
        
        student_data = db_handler.get_all_data_from_students()
        enrollment_data = db_handler.get_all_data_from_enrollments()
        class_data = db_handler.get_all_data_from_classes()
        
        # getting student_id from clicked href link
        student_id = request.args.get('student_id', type=int)
        print(f"Selected Student: {student_id} (ID)")
        
        found_student = None
        found_enrollment_data = []
        found_class_data = []
        
        enrollment_found = False
        
        # finding student data
        for student in student_data:
            if student.student_id == student_id:
                found_student = student
                print(f"Student Found: {found_student.first_name} {found_student.last_name}")
        
        # finding enrollment data    
        if found_student:
            for enrollment in enrollment_data:
                if enrollment.student_id == found_student.student_id:
                    found_enrollment_data.append(enrollment)
                    enrollment_found = True
                    print(f"Enrollment Added: {enrollment.enrollment_id} (ID)")
        
        # finding enrolled class data         
        if found_enrollment_data:
            for classe in class_data:
                for enrollment in found_enrollment_data:
                    if classe.class_id == enrollment.class_id:
                        found_class_data.append(classe)
                        print(f"Class Added: {classe.class_name}")
        
        # redirecting if no enrollment data found              
        if enrollment_found is False:
            found_enrollment_data.append("No Enrollments Found")
            found_class_data.append("No Classes Found")
            print(f"No Enrollments Found: {found_student.first_name} {found_student.last_name} ")
            return render_template('student_profile.html', found_student=found_student, found_enrollment_data=found_enrollment_data, found_class_data=found_class_data)
        
        return render_template('student_profile.html', found_student=found_student, found_enrollment_data=found_enrollment_data, found_class_data=found_class_data, enrollment_found=enrollment_found)
    
        

#----------------------- EMPLOYEE PROFILE

@app.route('/employee_profile', methods=['POST'])
def employee_profile():
    if request.method == 'POST':
        
        employee_data = db_handler.get_all_data_from_employees()
        enrollment_data = db_handler.get_all_data_from_enrollments()
        class_data = db_handler.get_all_data_from_classes()
        student_data = db_handler.get_all_data_from_students()
        
        employee_id = int(request.form['employee_id'])
        print(f"Selected Employee: {employee_id} (ID)")
        
        found_employee = None
        found_enrollment_data = []
        found_class = None
        
        enrollment_found = False
        
        # finding employee data
        for employee in employee_data:
            if employee.employee_id == employee_id:
                found_employee = employee
                print(f"Employee Found: {found_employee.first_name} {found_employee.last_name}")
        
        # finding enrollment data    
        if found_employee:
            for enrollment in enrollment_data:
                if enrollment.employee_id == found_employee.employee_id:
                    found_enrollment_data.append(enrollment)
                    enrollment_found = True
                    print(f"Enrollment Added: {enrollment.enrollment_id} (ID)")
        
        # finding enrolled class data         
        if found_enrollment_data:
            for classe in class_data:
                if classe.class_id == found_employee.class_id:
                    found_class = classe
                    print(f"Class Found: {classe.class_name}")
    
        # redirecting if no enrollment data found              
        if enrollment_found is False:
            found_enrollment_data.append("No Enrollments Found")
            found_class = "No Classes Found"
            print(f"No Enrollments Found: {found_employee.first_name} {found_employee.last_name} ")
            return render_template('employee_profile.html', found_employee=found_employee, found_enrollment_data=found_enrollment_data, found_class=found_class)
        
        return render_template('employee_profile.html', found_employee=found_employee, found_enrollment_data=found_enrollment_data, found_class=found_class, enrollment_found=enrollment_found, student_data=student_data, class_data=class_data, employee_data=employee_data, enrollment_data=enrollment_data)

    
#----------------------- CLASS PROFILE

@app.route('/class_profile', methods=['GET','POST'])
def class_profile():
    if request.method == 'POST':
        
        enrollment_data = db_handler.get_all_data_from_enrollments()
        class_data = db_handler.get_all_data_from_classes()
        employee_data = db_handler.get_all_data_from_employees()
        student_data = db_handler.get_all_data_from_students()
        
        class_id = int(request.form['class_id'])
        print(f"Selected Class: {class_id} (ID)")
        
        found_class = None
        found_employee = None
        found_enrollment_data = []
        
        
        enrollment_found = False
        
        # finding class data
        for classe in class_data:
            if classe.class_id == class_id:
                found_class = classe
                print(f"Class Found: {found_class.class_name}")
        
        
        # finding enrollment data    
        if found_class:
            for enrollment in enrollment_data:
                if enrollment.class_id == found_class.class_id:
                    found_enrollment_data.append(enrollment)
                    enrollment_found = True
                    print(f"Enrollment Added: {enrollment.enrollment_id} (ID)")
        
        
        # finding enrolled employee data         
        if found_enrollment_data:
            for employee in employee_data:
                if found_class.class_id == employee.class_id:
                    found_employee = employee
                    print(f"Employee Found: {employee.first_name} {employee.last_name}")
    
        
        # redirecting if no enrollment data found              
        if enrollment_found is False:
            found_enrollment_data.append("No Enrollments Found")
            print(f"No Enrollments Found: {found_class.class_name}")
            return render_template('class_profile.html', found_employee=found_employee, found_enrollment_data=found_enrollment_data, found_class=found_class)
        
        return render_template('class_profile.html', found_employee=found_employee, found_enrollment_data=found_enrollment_data, found_class=found_class, enrollment_found=enrollment_found, student_data=student_data, class_data=class_data, employee_data=employee_data, enrollment_data=enrollment_data )

    if request.method == 'GET':
        
        enrollment_data = db_handler.get_all_data_from_enrollments()
        class_data = db_handler.get_all_data_from_classes()
        employee_data = db_handler.get_all_data_from_employees()
        student_data = db_handler.get_all_data_from_students()
        
        class_id = request.args.get('class_id', type=int)
        print(f"Selected Class: {class_id} (ID)")
        
        found_class = None
        found_employee = None
        found_enrollment_data = []
        
        
        enrollment_found = False
        
        # finding class data
        for classe in class_data:
            if classe.class_id == class_id:
                found_class = classe
                print(f"Class Found: {found_class.class_name}")
        
        
        # finding enrollment data    
        if found_class:
            for enrollment in enrollment_data:
                if enrollment.class_id == found_class.class_id:
                    found_enrollment_data.append(enrollment)
                    enrollment_found = True
                    print(f"Enrollment Added: {enrollment.enrollment_id} (ID)")
        
        
        # finding enrolled employee data         
        if found_enrollment_data:
            for employee in employee_data:
                if found_class.class_id == employee.class_id:
                    found_employee = employee
                    print(f"Employee Found: {employee.first_name} {employee.last_name}")
    
        
        # redirecting if no enrollment data found              
        if enrollment_found is False:
            found_enrollment_data.append("No Enrollments Found")
            print(f"No Enrollments Found: {found_class.class_name}")
            return render_template('class_profile.html', found_employee=found_employee, found_enrollment_data=found_enrollment_data, found_class=found_class)
        
        return render_template('class_profile.html', found_employee=found_employee, found_enrollment_data=found_enrollment_data, found_class=found_class, enrollment_found=enrollment_found, student_data=student_data, class_data=class_data, employee_data=employee_data, enrollment_data=enrollment_data )



# ADMIN -------------------------------------------------------------------------



@app.route('/admin')
def admin_page():
    
    student_data = db_handler.get_all_data_from_students()
    class_data = db_handler.get_all_data_from_classes()
    employee_data = db_handler.get_all_data_from_employees()
    enrollment_data = db_handler.get_all_data_from_enrollments()
    user_data = db_handler.get_all_data_from_users()
    
    return render_template("admin.html", student_data=student_data, class_data=class_data, employee_data=employee_data, enrollment_data=enrollment_data, user_data=user_data)
# simple CRUD interface

#----------------------- DELETE

@app.route('/delete_students', methods=['POST'])
def admin_delete_students():
    if request.method == 'POST':
        
        # retrieving all student data
        student_data = db_handler.get_all_data_from_students()
        enrollment_data = db_handler.get_all_data_from_enrollments()
        
        inputted_student_id = int(request.form['student_id'])

        found_student = None
        found_enrollment_data = []
        
        enrollment_found = False
        
        # searching for student 
        for student in student_data:
            if student.student_id == inputted_student_id:
                found_student = student
                print(f"Found Student: {found_student.first_name} {found_student.last_name}")
                
        # searching for enrollments associated with student
        for enrollment in enrollment_data:
            if found_student.student_id == enrollment.student_id:
                found_enrollment_data.append(enrollment)
                enrollment_found = True
                print(f"Enrollment {enrollment.enrollment_id} Added (ID)")
        
             
        # removing student (if found)
        # removing any enrollments associated with student    
        if enrollment_found:
            for enrollment in enrollment_data:
                db_handler.remove_from_enrollments(enrollment)
                print(f"{enrollment} Deleted")
            db_handler.remove_from_students(found_student)
            print(f"{found_student.first_name} {found_student.last_name} Deleted")
            flash(f'{found_student.first_name} {found_student.last_name} Deleted Successfully', 'student_deleted')
        
        # removing student (if enrollment isn't found)
        if not enrollment_found:
            db_handler.remove_from_students(found_student)
            print(f"No Enrollments Found for {found_student.first_name} {found_student.last_name}")
            print(f"{found_student.first_name} {found_student.last_name} Deleted Successfully")
            flash(f'{found_student.first_name} {found_student.last_name} Deleted Successfully', 'student_deleted')
        
        
            
        
        return redirect(url_for('admin_page'))
        

@app.route('/delete_employees', methods=['POST'])
def admin_delete_employees():
    if request.method == 'POST':
        
        employee_data = db_handler.get_all_data_from_employees()
        enrollment_data = db_handler.get_all_data_from_enrollments()
        
        
        
        inputted_employee_id = int(request.form['employee_id'])
        
        found_employee = None
        found_enrollment_data = []
        
        enrollment_found = False
        
        # searching for selected employee
        for employee in employee_data:
            if employee.employee_id == inputted_employee_id:
                found_employee = employee
                
        # searching for enrollments associated with employee
        for enrollment in enrollment_data:
            if found_employee.employee_id == enrollment.employee_id:
                found_enrollment_data.append(enrollment)
                enrollment_found = True
                print(f"Enrollment {enrollment.enrollment_id} Added (ID)")
                
        # removing any enrollments associated with student      
        if found_enrollment_data:
            for enrollment in found_enrollment_data:
                db_handler.remove_from_enrollments(enrollment)
                print(f"{enrollment} Deleted")
        
        # removing employee (if found)  
        if found_employee:
            db_handler.remove_from_employees(found_employee)
            flash(f'{found_employee.first_name} {found_employee.last_name} Deleted Successfully', 'student_deleted')
        
        # removing employee (if enrollment isn't found)
        if not enrollment_found:
            db_handler.remove_from_employees(found_employee)
            print(f"No Enrollments Found for {found_employee.first_name} {found_employee.last_name}")
            print(f"{found_employee.first_name} {found_employee.last_name} Deleted Successfully")
        
        if found_employee is None:
            print("Employee Not Found")
            flash('Employee Not Found', 'student_not_found')

        return redirect(url_for('admin_page'))


@app.route('/delete_users', methods=['POST'])
def admin_delete_users():
    if request.method == 'POST':
        
        # retrieving all user data
        user_data = db_handler.get_all_data_from_users()
        
        inputted_user_id = int(request.form['user_id'])
        
        found_user = None
        
        # searching for user
        for user in user_data:
            if user.user_id == inputted_user_id:
                found_user = user
                db_handler.remove_from_users(found_user)
                print(f"Found User: {found_user.first_name} {found_user.last_name}")
                flash(f'User {found_user.first_name} {found_user.last_name} Deleted Successfully', 'student_deleted')
                
        if found_user is None:
            print(f"User ID {inputted_user_id} Not Found ")
            flash('User Not Found', 'student_not_found')

        return redirect(url_for('admin_page'))
    
    return redirect(url_for('admin_page'))


@app.route('/delete_classes', methods=['POST'])
def admin_delete_classes():
    if request.method == 'POST':
        
        # retrieving all class data
        class_data = db_handler.get_all_data_from_classes()
        employee_data = db_handler.get_all_data_from_employees()
        enrollment_data = db_handler.get_all_data_from_enrollments()
        
        
        inputted_class_id = int(request.form['class_id'])
         
        
        found_class = None
        found_employee = None
        found_enrollment_data  = []
        
        employee_found = False
        
        
        # finding class to remove
        for classe in class_data:
            if classe.class_id == inputted_class_id:
                found_class = classe
                print(f"Found Class: {found_class.class_id}")
                break
                
        # finding associated employee
        for employee in employee_data:
            if found_class.class_id == employee.class_id:
                found_employee = employee
                employee_found = True
                print(f"Found Employee ID: {found_employee.employee_id}")
                break
            
        # finding associated enrollments
        for enrollment in enrollment_data:
            if found_class.class_id == enrollment.class_id:
                found_enrollment_data.append(enrollment)
                

        # removing enrollments associated with the associated employee
        if found_enrollment_data:
            for enrollment in found_enrollment_data:
                db_handler.remove_from_enrollments(enrollment)
                print(f"{enrollment} Deleted")

        # removing class_id from associated employee
        if found_employee:
            found_employee.class_id = None
            db_handler.remove_from_employees(found_employee)
            print(f"{found_employee.first_name} {found_employee.last_name} Removed")
            db_handler.insert_into_employees(first_name=found_employee.first_name, last_name=found_employee.last_name, position=None, job=found_employee.job, class_id=found_employee.class_id)
            print(f"{found_employee.first_name} {found_employee.last_name} Added")
       
        # jumps to deleting class if no employee association is found
        if not employee_found:
                db_handler.remove_from_classes(found_class)
                print(f"{found_class.class_name} Removed")
                flash(f'{found_class.class_name} Deleted Successfully', 'student_deleted')
                return redirect(url_for('admin_page'))
        
        db_handler.remove_from_classes(found_class)
        
                      
        flash(f'{found_class.class_name} Deleted Successfully', 'student_deleted')
        return redirect(url_for('admin_page'))
        
    return redirect(url_for('admin_page'))

@app.route('/delete_enrollments', methods=['POST'])
def admin_delete_enrollments():
    if request.method == 'POST':
        
        student_data = db_handler.get_all_data_from_students()
        enrollment_data = db_handler.get_all_data_from_enrollments()
        
        # inputted_student_email = request.form['student_email'].lower()
        inputted_student_id = int(request.form['student_id'])
        
        found_student = None 
        found_enrollment_data = []
        
        enrollment_removed = False
        enrollment_found = False
        
        
        # searching for student
        for student in student_data:
            if student.student_id == inputted_student_id:
                found_student = student
                print(f"Found Student: {found_student.first_name} {found_student.last_name}")
                        
                
        # searching for enrollments associated with student
        for enrollment in enrollment_data:
            if found_student.student_id == enrollment.student_id:
                found_enrollment_data.append(enrollment)
                enrollment_found = True
                print(f"Enrollment {enrollment.enrollment_id} Added (ID)")
        
        # removing student enrollments (if found) 
        if found_student and enrollment_found:
            for enrollment in found_enrollment_data:
                db_handler.remove_from_enrollments(enrollment)
                enrollment_removed = True
                print(f"{enrollment} Deleted")
                
        if enrollment_removed:
            flash(f'Enrollments for {found_student.first_name} {found_student.last_name} Deleted', 'student_deleted')
        else:
            flash(f'No Enrollments Found', 'student_not_found') 
            
            
        if not found_student:
            flash('Student Not Found', 'student_not_found') 
    
        return redirect(url_for('admin_page'))
    
    return redirect(url_for('admin_page'))
    
    



#----------------------- ADD

@app.route('/add_students', methods=['POST'])
def admin_add_students():
    if request.method == 'POST':
        
        student_email = f"{request.form['first_name'][0]}{request.form['last_name']}{randint(0,99)}@gmail.com".lower()
        # generating a student email
        
        
        # sending form data to database
        db_handler.insert_into_students(
            first_name = request.form['first_name'],
            last_name = request.form['last_name'],
            grade = request.form['grade'],
            age = request.form['age'],  
            student_email = student_email
            )
        
        
        flash(f'Student Added Successfully | Student Email: {student_email}', 'student_added')
        return redirect(url_for('admin_page'))
    
    
    return redirect(url_for('admin_page'))

@app.route('/add_employees', methods=['POST'])
def admin_add_employees():
    if request.method == 'POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        db_handler.insert_into_employees(
            first_name = first_name,
            last_name = last_name,
            position = "n/a",
            job = request.form['job'],
            class_id = None
            )
        
        flash(f'{first_name} {last_name} Added Successfully', 'student_added')
        return redirect(url_for('admin_page'))

    return redirect(url_for('admin_page'))

@app.route('/add_classes', methods=['POST'])
def admin_add_classes():
    if request.method == 'POST':
        
        
        class_name = request.form['class_name']
        employee_id = int(request.form['employee_id'])
        print(employee_id)

        db_handler.insert_into_classes(
            class_name = class_name, 
            room_number = request.form['room_number'],
            period = request.form['class_period'],
            )
        
        class_data = db_handler.get_all_data_from_classes()
        
        found_class = None
        found_employee = None
        
        for classe in class_data:
            if classe.class_name == class_name:
                found_class =  classe
                print(found_class)
                break
                
        employee_data = db_handler.get_all_data_from_employees()        
                
        for employee in employee_data:
            if employee.employee_id == employee_id:
                found_employee = employee 
                print(found_employee)
                break
                
        if found_employee and found_class:
            print(f'Before update - Employee ID: {found_employee.employee_id}, Class ID: {found_employee.class_id}')
            found_employee.class_id = found_class.class_id
            print(f'After update - Employee ID: {found_employee.employee_id}, Class ID: {found_employee.class_id}')

            
            db_handler.remove_from_employees(found_employee)
            db_handler.insert_into_employees(first_name=found_employee.first_name, last_name=found_employee.last_name, position=None, job=found_employee.job, class_id=found_employee.class_id)     
        
        flash(f'{class_name} Added Successfully', 'student_added')
        return redirect(url_for('admin_page'))

    return redirect(url_for('admin_page'))

@app.route('/add_enrollments', methods=['POST'])
def admin_add_enrollments():
    
    if request.method == 'POST':
        
        class_data = db_handler.get_all_data_from_classes()
        employee_data = db_handler.get_all_data_from_employees()
        
        found_class = None
        found_employee = None
        
        # finding class to enroll
        for classe in class_data:
            if classe.class_id == int(request.form['class_id']):
                found_class = classe
                print(f"Found Class: {found_class}")
            
        # finding employee to enroll based on class   
        for employee in employee_data:
            if employee.class_id == found_class.class_id:
                found_employee = employee
                print(f"Found Employee: {found_employee}")
                
        employee_id = found_employee.employee_id
        period = found_class.period
    
        db_handler.insert_into_enrollments(
            student_id = int(request.form['student_id']),
            class_id = found_class.class_id,
            employee_id=employee_id,
            period=period
    )
        
        flash(f'Student Successfully Enrolled | Class: {found_class.class_name}, Teacher: {found_employee.first_name} {found_employee.last_name}, Period: {period}', 'student_deleted')
        return redirect(url_for('admin_page'))

    return redirect(url_for('admin_page'))


if __name__ == '__main__':
    app.run(debug=True)