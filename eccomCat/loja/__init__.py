from flask import Flask


app = Flask(__name__)

from loja.admin import rotas
# cur = db.cursor()
# teste= cur.execute('SELECT * FROM fashion')
# envio = teste.fetchall()
# print(envio)


