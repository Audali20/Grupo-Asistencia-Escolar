from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

#MySQL Connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Emerson"
app.config["MYSQL_DB"] = "Login"
mysql = MySQL(app)

# Settings
app.secret_key = "mysecretkey"

@app.route("/")
def pagina_principal():
    return render_template("proyecto.html")

@app.route("/Registro")
def Index():
    return render_template("Registro_D.html")

@app.route("/Home")
def Home_us():
    return render_template("interfaz1.html")

#Conexion al Login
@app.route("/Add_docente", methods = ["POST"])
def add_user():
    if request.method == "POST":
        Nombre = request.form["Nombre"]
        Apellido = request.form["Apellido"]
        Correo = request.form["Correo"]
        Contraseña = request.form["Contraseña"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Registro_docentes (Nombre, Apellido, Correo, Contraseña) VALUES (%s, %s, %s, %s)", 
        (Nombre, Apellido, Correo, Contraseña))
        mysql.connection.commit()
        flash("Registered successfully!")
        return redirect(url_for("Home_us"))



@app.route("/RegistroEstudiantes")
def Create_asistencia():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Registro_estudiantes")
    data = cur.fetchall()
    return render_template("Registro_E.html", estudiantes = data)


# Conexion para añadir estudiantes a la BD de la lista
@app.route("/Add_estudiante", methods = ["POST"])
def add_estudiante():
    if request.method == "POST":
        NIE = request.form["NIE"]
        Nombre = request.form["Nombre"]
        Apellido = request.form["Apellido"]
        Correo = request.form["Correo"]
        Id_docente = request.form["Id_docente"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Registro_estudiantes (NIE, Nombre, Apellido, Correo, Id_docente) VALUES (%s, %s, %s, %s, %s)", 
        (NIE, Nombre, Apellido, Correo, Id_docente))
        mysql.connection.commit()
        flash("Successfully registered student!")
        return redirect(url_for("Create_asistencia"))


# Lista de estudiantes
# @app.route("/Lista")
# def Lista_3A():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM Registro_asistencia")
#     data = cur.fetchall()
#     print(data)
#     return render_template("Lista.html", asistencia = data)

# Conexion a la DB Registro_asistencias
# @app.route("/Add_asistencia", methods = ["POST"])
# def add_asistencia():
#     if request.method == "POST":
#         NIE = request.form["NIE"]
#         Nombre = request.form["Nombre"]
#         Apellido = request.form["Apellido"]
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO registro_asistencia(NIE, Nombre, Apellido) SELECT DISTINCT(%s), %s, %s FROM Registro_estudiantes", 
#         (NIE, Nombre, Apellido))
#         mysql.connection.commit()
#         return redirect(url_for("Lista_3A"))



@app.route("/edit/<NIE>")
def get_asistencia(NIE):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Registro_estudiantes WHERE NIE = {0}".format(NIE))
    data = cur.fetchall()
    return render_template("Edit-estudiantes.html", estudiante = data[0])

@app.route("/update/<NIE>", methods = ["POST"])
def update_estudiante(NIE):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        Nombre = request.form["Nombre"]
        Apellido = request.form["Apellido"]
        Correo = request.form["Correo"]
        Id_docente = request.form["Id_docente"]
        cur.execute("""
        UPDATE Registro_estudiantes
        SET Nombre = %s,
            Apellido = %s,
            Correo = %s,
            Id_docente = %s
        WHERE NIE = %s
        """, (Nombre, Apellido, Correo, Id_docente, NIE))
        mysql.connection.commit()
        flash("Successfully upgraded student!")
        return redirect(url_for("Create_asistencia"))

@app.route("/delete/<string:NIE>")
def delete_asistencia(NIE):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Registro_estudiantes WHERE NIE = {0}".format(NIE))
    mysql.connection.commit()
    return redirect(url_for("Create_asistencia"))

if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.run(port = 3000, debug = True)
