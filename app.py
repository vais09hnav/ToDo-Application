from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "siva"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
app.secret_key = "abc123"

# Home Route - Displays all tasks
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM todoapp"
    con.execute(sql)
    res = con.fetchall()
    con.close()  # Always close the cursor
    return render_template("index.html", datas=res)

# Add Task Route - Adds a new task
@app.route("/addtask", methods=['GET', 'POST'])
def addtask():
    if request.method == 'POST':
        id = request.form['ID']
        date = request.form['DATE']
        task = request.form['TASK']
        time = request.form['TIME']
        
        con = mysql.connection.cursor()
        sql = "INSERT INTO todoapp (ID, DATE, TASK, TIME) VALUES (%s, %s, %s, %s)"
        con.execute(sql, (id, date, task, time))
        mysql.connection.commit()
        con.close()
        flash('Task Added Successfully')        
        return redirect(url_for("home"))
    return render_template("addtask.html")

# Edit Task Route - Updates an existing task
@app.route("/edittask/<int:id>", methods=['GET', 'POST'])
def edittask(id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        date = request.form['DATE']
        task = request.form['TASK']
        time = request.form['TIME']
        
        sql = "UPDATE todoapp SET DATE = %s, TASK = %s, TIME = %s WHERE ID = %s"
        con.execute(sql, (date, task, time, id))
        mysql.connection.commit()
        con.close()
        flash('Task Updated Successfully')
        return redirect(url_for("home"))
    else:
        # Fetch existing task details for editing
        sql = "SELECT * FROM todoapp WHERE ID = %s"
        con.execute(sql, (id,))
        task_data = con.fetchone()
        con.close()
        return render_template("edittask.html", task=task_data)

# Delete Task Route - Deletes a task by ID
@app.route("/deletetask/<int:id>", methods=['POST'])
def deletetask(id):
    con = None
    try:
        con = mysql.connection.cursor()
        sql = "DELETE FROM todoapp WHERE ID = %s"
        con.execute(sql, (id,)) 
        mysql.connection.commit()
        flash('Task Deleted Successfully')
    except Exception as e:
        flash(f"Error occurred while deleting task: {e}")
    finally:
        if con is not None:
            con.close()  
    return redirect(url_for("index.html"))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
