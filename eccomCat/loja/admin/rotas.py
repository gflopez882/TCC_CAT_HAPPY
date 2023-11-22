
import sqlite3
from loja import app
from flask import render_template, abort, session, request, url_for, redirect


app.secret_key ='!@#matodentro@#'

#-------------- Conectar ao banco--------------------
banco = 'cathappy.db'

def conectar_banco(banco):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    return conexao, cursor

def fechar_banco(conexao):
    print('teste certo')
    conexao.commit()
    conexao.close()
    



@app.route('/')
def home():
    return render_template("/index/index.html", title="Home")


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session.pop('user_name', '')
        email = request.form.get('email')
        senha = request.form.get('senha')

    #------------------Query verificar usuario ------------------------------------------------
        conexao, cursor = conectar_banco(banco)
        query = f"SELECT * FROM user WHERE email = '"+email+"' AND password = '"+senha+"'"
        user_loc = cursor.execute( query)
        user= user_loc.fetchone()
        
        
        if user:
            session['id'] = user[0]
            session['email'] = email
            session['name'] = user[1]
            fechar_banco(conexao)
            # print(session)
            return redirect('/')
    return render_template("/login/login.html", title="Login")


@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        senha = request.form.get('password')
        print(f'\n{fname}\n{lname}\n{email}\n{senha}')
        conexao, cursor = conectar_banco(banco)
        cursor.execute("INSERT INTO User (fname, lname, email, password) VALUES ( ?, ?, ?, ?);", (fname, lname, email, senha))
        fechar_banco(conexao)
        return redirect("/login/")
        
    return render_template("/login/signup.html", title="register")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/recuperar_senha/')
def recuperar_senha():
    return render_template("/login/forgot_password.html", title="recuperar senha")


@app.route('/produtos/acessorios/')
def produtos_po():
    conexao, cursor = conectar_banco(banco)
    itens = cursor.execute( "SELECT * FROM acessorios")
    products = itens.fetchall()
    #print(products)

    return render_template("/produtos/list.html", products = products, title="acessorios")


@app.route('/produtos/brinquedos/')
def produtos_graos():
    conexao, cursor = conectar_banco(banco)
    itens = cursor.execute( "SELECT * FROM brinquedos")
    products = itens.fetchall()
    #print(products)

    return render_template("/produtos/list.html", products = products, title="brinquedos")


@app.route('/produtos/alimentos/')
def produtos_capsula():
    conexao, cursor = conectar_banco(banco)
    itens = cursor.execute( "SELECT * FROM alimentos")
    products = itens.fetchall()
    #print(products)

    return render_template("/produtos/list.html", products = products, title="alimentos")


@app.route('/produtos/cuidados/')
def produtos_soluvel():
    conexao, cursor = conectar_banco(banco)
    itens = cursor.execute( "SELECT * FROM cuidados")
    products = itens.fetchall()
    #print(products)

    return render_template("/produtos/list.html", products = products, title="cuidados")


@app.route("/produtos/<product>/<product_id>")
def view_product(product, product_id):

    conexao, cursor = conectar_banco(banco)
    res = cursor.execute(f"""
                            SELECT * FROM {product.lower()}
                            WHERE id = {product_id}
                        """)
    envio = res.fetchone()
    #print(f'\n\n\n{envio[1]}\n\n\n')

    if envio == False:
        abort(404)
    else:
        return render_template(
            "/produtos/view.html",
            results= envio,
            title=envio[1],
        )


# @app.route("/carrinho/<product>/<product_id>")
# def view_product(product, product_id):
#     return 'helo'
@app.route('/create')
def create():
    if session:
        item = request.args.to_dict()
        user = session['id']
        item["id_user"] = session['id']
        # print(item)
        # print(user)
        conexao, cursor = conectar_banco(banco)
        res = cursor.execute(f"""INSERT INTO carrinho ( name, quant, valor, id_user, img_url, tamanho ) VALUES ( :name, :quant, :valor, :id_user, :img_url, :tamanho )""", item)
        fechar_banco(conexao)
        return redirect(request.referrer)
    return redirect('/login')


@app.route('/delete/<id_item>')
def delete(id_item):
    conexao, cursor = conectar_banco(banco)
    res = cursor.execute(f"""DELETE FROM carrinho WHERE id = {id_item}""")
    fechar_banco(conexao)
    return redirect('/carrinho/')


@app.route('/carrinho/')
def carrinho():
    if session:
        user_id = session['id']
        print(f'Usuario {user_id}')
        conexao, cursor = conectar_banco(banco)
        itens_cart = cursor.execute(f"""
                            SELECT * FROM carrinho
                            WHERE id_user = {user_id}
                        """)
        envio = itens_cart.fetchall()
        # print(f'envio = {envio}')

        total = 0

        for item in envio:
            total += item[2] * item[3]
            print(f'quant = {item[2]} -- val {item[3]}')
        # print(total)

        return render_template("/carrinho/carrinho.html", items = envio, total = total, title="Carrinho")

    return render_template("/carrinho/carrinho.html", title="Carrinho")


#------------------------------------carrinho Dados ------------------------------------------------------------#

