from flask import Flask, jsonify, request, session, abort, flash, redirect
import os
import pyodbc as db

#padrões para a conexão com o banco de dados
server = 'LAPTOP-JVVCVHHD'
database = 'HackStudying'
username = ''
password = ''
driver= '{ODBC Driver 13 for SQL Server}'


#CONECTA AO BANCO DE DADOS
con = db.connect('DRIVER='+ driver+';SERVER='+server+';Trusted_Connection=yes;DATABASE='+database)
cur = con.cursor()

app = Flask(__name__)

#teste padrão tela inicial
@app.route('/')
def api_root():
    if not session.get('logged_in'):
        return "intruso"
    else:
        return "Hello Boss!"
#retorna o JSON de um cliente com id X
@app.route('/cliente/<id>', methods=['GET'])
def api_article(id):
    qry = 'select * from dbo.Cliente where idCliente = ' + str(id)
    cur.execute(qry)
    row = cur.fetchone()
    cliente = {"idCliente": str(row[0]), "login": str(row[1]).replace(" ", ""), "senha": str(row[2]).replace(" ", ""),"nome": str(row[3]).replace("  ", ""), "sexo": str(row[4]).replace(" ", ""), "data_nasc": str(row[5]).replace(" ", ""), "email": str(row[6]).replace(" ", "") }
    return jsonify(cliente)

#Cadastra um cliente
@app.route('/cadastrarCliente/', methods=['POST'])
def cadastrarCliente():
    if request.method == "POST":
        #Pegando os dados do POST
        login = str(request.form.get('login'))
        senha = str(request.form.get('senha'))
        nome = str(request.form.get('nome'))
        sexo = str(request.form.get('sexo'))
        data_nasc = str(request.form.get('data_nasc'))
        email = str(request.form.get('email'))
        qry = "INSERT INTO dbo.Cliente(login,senha,nome,sexo, data_nasc,email) Values ('"+login+"','"+senha+"','"+nome+"',"+sexo+",'"+data_nasc+"','"+email+"')"
        status = ''
        try:
            cur.execute(qry)
            cur.commit()

            
            qry = "SELECT idCliente FROM dbo.Cliente WHERE login ='"+login+"' and senha ='"+senha+"'"
            cur.execute(qry)
            row = cur.fetchone()
            id1 = str(row[0]).replace(" ","")
            print(id1)
            qry = "INSERT INTO dbo.ConfigCliente(idCliente,qtdRespondidas,qtdCertas,qtdErradas) Values ("+str(id1)+","+str(0)+","+str(0)+","+str(0)+")"
            print(qry)
            print("qry")
            cur.execute(qry)
            print(qry)
            cur.commit()
            
            status = "True"
        except :
            status = 'False'
        return redirect("http://localhost:4200/", code=302)

#Entrar com Login e Senha
@app.route('/entrar/', methods=['POST'])
def entrar():
    if request.method == "POST":
        #Pegando os dados do POST
        login = str(request.form.get('login'))
        senha = str(request.form.get('senha'))
        qry = "SELECT idCliente, login,senha FROM dbo.Cliente WHERE login ='"+login+"' and senha ='"+senha+"'"
        status = ''
        try:
            cur.execute(qry)
            
            row = cur.fetchone()
            
            if login == str(row[1]).replace(" ", "") and senha== str(row[2]).replace(" ", ""):
               
                session['logged_in'] = True
                status = "True"
                print("autenticou")
                return redirect("http://localhost:4200/dashboard/"+str(row[0]), code=302)
            else: 
                status = "False" 
                flash('wrong password!')

        except:
            status = "False"
    return status

#esqueci senha
@app.route('/esquecisenha/', methods=['POST'])
def esquecisenha():
    if request.method == "POST":
        #Pegando os dados do POST
        email = str(request.form.get('email'))
        novaSenha = str(request.form.get('novasenha'))
        qry = "SELECT idCliente, email FROM dbo.Cliente WHERE email ='"+email+"'"
        status = ''
        try:
            cur.execute(qry)
            row = cur.fetchone()
            print(row[1])
            if email == str(row[1]).replace(" ", ""): 
                status = "True"
                
                qry = "UPDATE dbo.Cliente SET senha ='"+novaSenha+"' WHERE idCliente = '"+str(row[0]).replace(" ", "")+"'"
                cur.execute(qry)
                cur.commit()
            else: status = "False" 
            
        except:
            status = "False"
    return status


#---------------Lidando com as Perguntas---------------------
#retorna o JSON de uma pergunta com id X
@app.route('/pergunta/<id>', methods=['GET'])
def getPergunta(id):
    qry = 'select * from dbo.Pergunta where idPergunta = ' + str(id)
    cur.execute(qry)
    row = cur.fetchone()
    pergunta = {"idPergunta": str(row[0]), "pergunta": str(row[1]).replace(" ", ""), "alternativaA": str(row[2]).replace(" ", ""),"alternativaB": str(row[3]).replace(" ", ""), "alternativaC": str(row[4]).replace(" ", ""), "alternativaCorreta": str(row[5]).replace(" ", ""), "nivel": str(row[6]).replace(" ", "") }
    return jsonify(pergunta)

#retorna o JSON de todas as perguntas
@app.route('/perguntas', methods=['GET'])
def getPerguntas():
    qry = 'select * from dbo.Pergunta'
    cur.execute(qry)
    row = cur.fetchone()
    perguntas = []
    while row:
        pergunta = {"idPergunta": str(row[0]), "pergunta": str(row[1]).replace("  ", ""), "alternativaA": str(row[2]).replace(" ", ""),"alternativaB": str(row[3]).replace(" ", ""), "alternativaC": str(row[4]).replace(" ", ""), "alternativaCorreta": str(row[5]).replace(" ", ""), "nivel": str(row[6]).replace(" ", "") }
        perguntas = perguntas+  [pergunta]
        row = cur.fetchone()
    return jsonify(perguntas)



#-------------------Trabalhando com a configuração do Cliente-------------
#atualiza a configuração de um cliente +
@app.route('/add1/<id>', methods=['GET'])
def add1(id):
    
    try:
        qry = "SELECT qtdRespondidas FROM ConfigCliente WHERE idCliente ='"+id+"'"
        cur.execute(qry)
        row = cur.fetchone()
        total = str(row[0]).replace(" ","")
        qry = "UPDATE dbo.ConfigCliente SET qtdRespondidas ="+str((int(total)+1))+" WHERE idCliente = "+str(id)
        cur.execute(qry)
        cur.commit()
    except:
        print("Kelwin Burro")
    return "OK"

#atualiza a configuração de um cliente -1
@app.route('/remove1/<id>', methods=['GET'])
def remove1(id):
    try:
        qry = "SELECT qtdRespondidas FROM ConfigCliente WHERE idCliente ='"+id+"'"
        cur.execute(qry)
        row = cur.fetchone()
        total = str(row[0]).replace(" ","")
        qry = "UPDATE dbo.ConfigCliente SET qtdRespondidas ="+str((int(total)-1))+" WHERE idCliente = "+str(id)
        cur.execute(qry)
        cur.commit()
    except:
        print("Kelwin Burro")
    return "OK"

#retorna CONFIGURAÇOES cliente X
@app.route('/configCliente/<id>', methods=['GET'])
def configCliente(id):
    try:
        qry = "SELECT qtdRespondidas FROM ConfigCliente WHERE idCliente ='"+id+"'"
        cur.execute(qry)
        row = cur.fetchone()
        total = str(row[0]).replace(" ","")
        
    except:
        print("Kelwin Burro")
    return total
    

if __name__ == '__main__':
  app.secret_key = os.urandom(12)
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)





