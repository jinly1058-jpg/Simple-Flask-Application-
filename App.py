from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'edu-pulse_secret_key'

# MySQL DB configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'studentdb'

# Initialize MySQL connection using the configured Flask application
mysql = MySQL(app)

# ------- ROUTE 1: VIEW ALL STUDENTS (READ) -------
@app.route('/')
def index():
    """
    Renders the home page (student directory dashboard)
    by fetching all records from the 'students' table.
    """
    try:
        # Create cursor to interact with the db
        cur = mysql.connection.cursor()
        
        # Execute query to fetch all student records
        cur.execute("SELECT * FROM students ORDER BY id DESC")
        data = cur.fetchall()
        
        # Close the connection cursor
        cur.close()
        
        # Render index.html with list of student records
        return render_template('index.html', students=data)
    except Exception as e:
      flash(f"Database connection error: {str(e)}. Please check if your MySQL server is running & the db is created.", "danger")
    return render_template('index.html', students=[])

# ---------- ROUTE 2: ADD NEW STUDENT (Create) ----------
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """
    GET: Displays the registration form to add a student.
    POST: Processes the form data and inserts a new student into the db.
    """
    if request.method == 'POST':
        # Retrieve form data submitted by the user
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        try:
            # Create a cursor to perform db insertion
            cur = mysql.connection.cursor()

            # Execute parameterized insert query to prevent SQL injection
            cur.execute("INSERT INTO students (name, email, course) VALUES (%s, %s, %s)", (name, email, course))

            # Commit the transaction to save changes to db
            mysql.connection.commit()

            # Close the connection cursor
            cur.close()

            # Display a success notification
            flash('Student registered successfully!', 'success')

            # Redirect back to the dashboard home page
            return redirect(url_for('index'))

        except Exception as e:
            flash(f"Error occurred while inserting student: {str(e)}", "danger")
            return redirect(url_for('index'))
          except Exception as e:
    # Handle cases where db is not running or wrong
    flash(f"Database connection error: {str(e)}. Please check if your MySQL server is running & the db is created.", "danger")
    return render_template('index.html', students=[])
    return render_template('add.html')

# ---------- ROUTE 3: edit student details (update) ----------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    """
    GET: Fetches the student details by ID and renders
         them inside the form.
    POST: Updates the student details in the db using
          the submitted form.
    """
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            # Retrieve updated form details
            name = request.form['name']
            email = request.form['email']
            course = request.form['course']

            # Execute parameterized update query
            cur.execute("UPDATE students SET name=%s, email=%s, course=%s WHERE id=%s", (name, email, course, id))
            mysql.connection.commit()
            cur.close()

            flash('Student details updated successfully!', 'success')
            return redirect(url_for('index'))
        
        else:
            # Execute SELECT query to fetch student details by ID
            cur.execute("SELECT * FROM students WHERE id=%s", (id,))
            student_data = cur.fetchone()
            cur.close()
            return render_template('edit.html', student=student_data)

    except Exception as e:
        flash(f"Error occurred: {str(e)}", "danger")
        return redirect(url_for('index'))

# ----- ROUTE 4: Delete Student (delete) -----
@app.route('/delete/<int:id>', methods=['GET'])
def delete_student(id):
    """
    Deletes the student matching the provided ID and redirects to the home page.
    """
    try:
        cur = mysql.connection.cursor()
        
        # Execute parameterized delete query
        cur.execute("DELETE FROM students WHERE id=%s", (id,))
        
        mysql.connection.commit()
        cur.close()
        
        flash('Student record deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting record: {str(e)}", "danger")
        
    return redirect(url_for('index'))

# Run the Flask app
if __name__ == '__main__':
    # set debug to True for auto-reload on changes
    app.run(debug=True)
  
