import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helper import login_required, usd, nio

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["nio"] = nio

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///banco.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    if request.method == "GET":
        if session["admin"] == False:
            user_id = session["user_id"]
            monto = db.execute("SELECT sum(monto) AS monto FROM cuenta WHERE user_id = ? group by user_id", user_id)[0]["monto"]
            cuenta = db.execute("SELECT t.descripcion AS tipo_cuenta, monto, m.descripcion AS moneda, numCuenta FROM cuenta c INNER JOIN tipo t ON (c.fkTipoCuenta = t.id) INNER JOIN moneda m ON (c.fkMoneda = m.id) WHERE user_id = ?", user_id)
            return render_template("index.html", monto=monto, cuenta=cuenta)

        else:
            return render_template("admin.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """"Register user"""
    if request.method == "GET":
        return render_template("registro.html")
    else:
        cedula = request.form.get("cedula")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        celular = request.form.get("celular")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmar")

        if not cedula or not nombre or not apellido or not celular or not username or not password or not confirmation  :
            flash("Campo Incompleto.", "error")
            return render_template("registro.html")


        if password != confirmation:
            flash("Contraseña diferente.", "error")
            return render_template("registro.html")


        hash = generate_password_hash(password)

        row = db.execute("SELECT username FROM usuario WHERE username = ?", username)
        if len(row) > 0:
            flash("Ya existe un usuario.", "error")
            return render_template("registro.html")

        new_user = db.execute("INSERT INTO usuario (cedula, nombre, apellido, celular, username, password) VALUES (?, ?, ?, ?, ?, ?)",cedula, nombre, apellido, celular, username, hash)

        session["user_id"] = new_user

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted`
        if not username or not password :
            flash("Campo Incompleto.", "error")
            return render_template("login.html")


        # Query database for username
        rows = db.execute("SELECT * FROM usuario WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            flash("La contra o username son incorrecto", "error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["admin"] = rows[0]["admin"]
        print(session["admin"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/solicitar_cuenta", methods=["GET", "POST"])
def solicitar():
    moneda = db.execute("SELECT * FROM moneda")
    tipo = db.execute("SELECT * FROM tipo")
    if request.method == "GET":

        return render_template("solicitar.html", moneda=moneda, tipo=tipo)

    else:
        tipoC = request.form.get("tipo")
        monedaC = request.form.get("moneda")

        if not moneda or not tipo:
            flash("Seleccione la solicitud.")
            return render_template("solicitar.html")

        cuenta = db.execute("SELECT * FROM cuenta WHERE user_id = ? AND fkMoneda = ? AND fkTipoCuenta = ?",session["user_id"], monedaC, tipoC)

        if len(cuenta) > 0:
            flash("Solicite nuevo requisitos", "error")
            return render_template("solicitar.html", moneda=moneda, tipo=tipo)

        solicitud = db.execute("SELECT * FROM solicitud WHERE user_id = ? AND fkMoneda = ? AND fkTipo = ?",session["user_id"], monedaC, tipoC)

        if len(solicitud) == 0:
            db.execute("INSERT INTO solicitud (user_id, fkMoneda, fkTipo, aprobacion) VALUES (?, ?, ?, ?)", session["user_id"], monedaC, tipoC, False)

        flash("Su solicitud a sido creada.", "exito")
        return redirect("/")

@app.route("/revisar_solicitud", methods=["GET", "POST"])
def revisar_solicitud():
    cuenta = db.execute("SELECT s.id, t.descripcion AS tipo_cuenta, u.nombre, m.descripcion AS moneda FROM solicitud s INNER JOIN tipo t ON (s.fkTipo = t.id) INNER JOIN moneda m ON (s.fkMoneda = m.id) INNER JOIN usuario u On (s.user_id = u.id) WHERE user_id = 1 AND aprobacion = 0 ")
    return render_template("revision.html", cuentas=cuenta)


@app.route("/aprobado", methods=["GET", "POST"])
def aprobar():
    id = request.args.get("id")
    aprobar = db.execute("SELECT * FROM solicitud WHERE id = ?", id)[0]
    moneda = aprobar["fkMoneda"]
    tipo = aprobar["fkTipo"]
    usuario = aprobar["user_id"]
    db.execute("INSERT INTO cuenta (monto, fkTipoCuenta, fkMoneda, user_id) VALUES (?, ?, ?, ?)",1 , tipo, moneda, usuario)
    db.execute("UPDATE solicitud SET aprobacion = ? WHERE id = ?", True, id)
    flash("Su cuenta ha sido aprobada", "exito")

    return redirect("/revisar_solicitud")

@app.route("/denegar", methods=["GET", "POST"])
def denegar():
    id = request.args.get("id")
    db.execute("DELETE FROM solicitud WHERE id = ?", id)
    flash("Solicitud denegada.", )
    return redirect("/revisar_solicitud")


@app.route("/enviar-dinero", methods=["GET", "POST"])
def transaccion():
    cuenta = db.execute("SELECT t.descripcion AS tipo_cuenta, monto, m.descripcion AS moneda, numCuenta FROM cuenta c INNER JOIN tipo t ON (c.fkTipoCuenta = t.id) INNER JOIN moneda m ON (c.fkMoneda = m.id) WHERE user_id = ?", session["user_id"])
    moneda = db.execute("SELECT * FROM moneda ")
    if request.method == "GET":

        return render_template("enviar.html", cuenta=cuenta, moneda=moneda)

    else:
        moneda1 = request.form.get("moneda")
        destino = request.form.get("cuentadest")
        nombre = request.form.get("destinatario")
        asunto = request.form.get("asunto")
        monto = request.form.get("monto")
        cuentao = request.form.get("cuentao")

        date = datetime.datetime.now()

        cuenta_destino = db.execute("SELECT * FROM cuenta WHERE numCuenta = ?", destino)

        if len(cuenta_destino) == 0:
            flash("Numero de cuenta invalido", "error")
            return render_template("enviar.html", cuenta=cuenta, moneda=moneda)


        db.execute("INSERT INTO transaccion (fecha, monto, fkCuentaOrigen, fkCuentaDestino, asunto) VALUES (?, ?, ?, ?, ?)",  date, monto, cuentao, destino, asunto)

        print(moneda1,destino, nombre, asunto, monto,cuentao)
        flash("Transaccion realizada", "exito")
        return redirect("/")


