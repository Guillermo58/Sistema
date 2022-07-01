import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helper import login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///banco.db")


# descripcion = "Ahorro facil"
# montoMaximo = 1000

fecha = "24-6-2022"
fkCuentaOrigen = "Lolita lazo"
monto = 100
fkCuentaDestino = "Estafany Rizo"

# monto = 100
# fkTipoCuenta = 1
# fkMoneda = 1
# user_id = 1
# numCuenta = 10020010000001

# fk_tipo_cuenta = 1
# moneda = 1
# num_cuenta = 10020010000001

# db.execute("INSERT INTO moneda (descripcion) VALUES (?)", descripcion)

# db.execute("INSERT INTO tipo (descripcion, montoMaximo) VALUES (?,?)", descripcion, montoMaximo)

# db.execute("INSERT INTO cuenta (numCuenta, monto, fkTipoCuenta, fkMoneda, user_id) VALUES (?, ?, ?, ?, ?)",  num_cuenta, monto, fk_tipo_cuenta, moneda, 1)

# db.execute("INSERT INTO transaccion (fecha, monto, fkCuentaOrigen, fkCuentaDestino) VALUES (?, ?, ?, ?)",  fecha, monto, fkCuentaOrigen, fkCuentaDestino)

cuentas =("Ahorro Ordinario","Ahorro Premia","Plan Ahorro Meta","Chiqui Ahorro","Remesas Xpress","Ahorro Euros",)

for cuenta in cuentas:
     db.execute("INSERT INTO tipo (descripcion, montoMaximo) VALUES (?,?)", cuenta, 1000)

