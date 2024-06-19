'''
Aluno: José Mateus Amaral de Mirada
'''


from flask import Flask,session
from flask_bcrypt import Bcrypt

#configurando o framework
app = Flask(__name__)
app.static_folder = 'assets'
app.secret_key = '1234567890987654321'
bcrypt = Bcrypt(app)

#importando o frontend e o backend
from . import frontend
from . import backend
from . import bd