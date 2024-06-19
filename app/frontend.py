import json
from flask import render_template,session,flash,request,redirect,url_for
from . import app
from . import bd


#Pagina inicial do site
@app.route("/")
def index():
    vagasBD = None
    if 'usuario' not in session:
        vagasBD = bd.queryVagas("SELECT * FROM vagas LIMIT 20;")
    else:
        vagasBD = bd.queryVagas("SELECT * FROM vagas WHERE usuario != ? LIMIT 20;",(session["usuario"],))
        for vaga in vagasBD:
            aplicacoes = json.loads(vaga["aplicacoes"])
            ok = True
            for aplicacao in aplicacoes:
                if aplicacao["usuario"] == session["usuario"]:
                    ok = False
                    break
            if not ok:
                vagasBD.remove(vaga)
    return render_template("index.html",vagasBD=vagasBD,semVagas=len(vagasBD)==0)



#Para mostrar as vagas do sistema e permite que o usuario use filtros para faciliar a procura de uma vaga
@app.route("/vagas", methods=["GET"])
def vagas():

    args = request.args
    codigo = args.get("codigo")
    estado = args.get("estado")
    cidade = args.get("cidade")
    carga_horaria = args.get("carga_horaria")
    modalidade = args.get("modalidade")
    tipo_contrato = args.get("tipo_contrato")
    area = args.get("area")

    query = "SELECT * FROM vagas WHERE usuario != ?"
    parametros = []
    if "usuario" in session:
        parametros.append(session["usuario"])
    else:
        parametros.append("x")
    if codigo != None:
        query += " AND id = ?"
        parametros.append(codigo)
    if estado != None: 
        query += " AND estado = ?"
        parametros.append(estado)
    if cidade != None: 
        query += " AND cidade = ?"
        parametros.append(cidade)

    if carga_horaria != None: 
        query += " AND carga_horaria = ?"
        parametros.append(carga_horaria)

    if modalidade != None: 
        query += " AND modalidade = ?"
        parametros.append(modalidade)

    if tipo_contrato != None: 
        query += " AND tipo_contrato = ?"
        parametros.append(tipo_contrato)

    if area != None: 
        query += " AND area = ?"
        parametros.append(area)
    query += ";"
    parametros = tuple(parametros)

    vagasBD = None
    if 'usuario' not in session:
        vagasBD = bd.queryVagas(query,parametros)
    else:
        vagasBD = bd.queryVagas(query,parametros)
        import json
        for vaga in vagasBD:
            aplicacoes = json.loads(vaga["aplicacoes"])
            ok = True
            for aplicacao in aplicacoes:
                if aplicacao["usuario"] == session["usuario"]:
                    ok = False
                    break
            if not ok:
                vagasBD.remove(vaga)

    import json
    with open('app/assets/dados/cidades_e_estados.json') as file:
        cidades_e_estados = json.load(file)
        erro = False
        mensagemErro = None
        if 'erroCadastro' in session:
            erro = True
            mensagemErro = session["mensagemErroCadastro"]
            del session["erroCadastro"]
            del session["mensagemErroCadastro"]
        
        return render_template("vagas.html",vagasBD=vagasBD,semVagas=len(vagasBD)==0,cidades_e_estados=cidades_e_estados)



#Pagina que mostra os dados de uma vaga. Ela tambem permite o gerenciamento da vaga caso o usuario atual tenha 
# criado a vaga
@app.route("/vaga/<idVaga>")
def vaga(idVaga):
    
    vagaDict = bd.queryVaga(idVaga)
    semAplicacoes = len(vagaDict["aplicacoes"]) == 0
    aplicado = False
    if 'usuario' in session:
        for aplicacao in vagaDict["aplicacoes"]:
            if aplicacao["usuario"] == session["usuario"]:
                aplicado = True
                break

    criador = False
    if 'usuario' in session:
        if session["usuario"] == vagaDict["usuario"]:
            criador = True

    if not criador:
        vagaDict["aplicacoes"] = []

    return render_template("vaga.html",vaga=vagaDict,semAplicacoes=semAplicacoes,criador=criador,aplicado=aplicado)



#Pagina para criar vagas. É necessário estar logado.
@app.route("/criar")
def criar():
    import json
    with open('app/assets/dados/cidades_e_estados.json') as file:
        cidades_e_estados = json.load(file)
        erro = False
        mensagemErro = None
        if 'erroCadastro' in session:
            erro = True
            mensagemErro = session["mensagemErroCadastro"]
            del session["erroCadastro"]
            del session["mensagemErroCadastro"]
        
        return render_template("criar.html",cidades_e_estados=cidades_e_estados)



#Pagina para editar uma vaga. Para editar uma vaga é necessário ser o proprietario
@app.route("/editar/<idVaga>")
def editar(idVaga):
    vaga = bd.queryVaga(idVaga)
    import json
    with open('app/assets/dados/cidades_e_estados.json') as file:
        cidades_e_estados = json.load(file)
        erro = False
        mensagemErro = None
        if 'erroCadastro' in session:
            erro = True
            mensagemErro = session["mensagemErroCadastro"]
            del session["erroCadastro"]
            del session["mensagemErroCadastro"]
        
        return render_template("editar.html",vaga=vaga,cidades_e_estados=cidades_e_estados)



#Para para editar os dados do perfil, como foto e dados pessoais
@app.route("/editarPerfil")
def editarPerfil():
    import json
    with open('app/assets/dados/cidades_e_estados.json') as file:
        
        cidades_e_estados = json.load(file)
        
        erro = False
        mensagemErro = None
        if 'erroCadastro' in session:
            erro = True
            mensagemErro = session["mensagemErroCadastro"]
            del session["erroCadastro"]
            del session["mensagemErroCadastro"]

        conn = bd.connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT email, estado, cidade, experiencia, formacao, aplicacoes, criacoes,dataNascimento, telefone, timestamp,genero, foto, nome FROM usuarios WHERE usuario = ?",(session["usuario"],))
        dadosBD = cursor.fetchone()
        usuario = bd.rowToDict(
            ['email','estado', 'cidade', 'experiencia', 'formacao', 'aplicacoes', 'criacoes', 'dataNascimento', 'telefone', 'timestamp','genero','foto','nome'],
            dadosBD
        )
        usuario["formacao"] = json.loads(usuario["formacao"])
        usuario["experiencia"] = json.loads(usuario["experiencia"])

        return render_template("editarPerfil.html",cidades_e_estados=cidades_e_estados,erro=erro,mensagemErro=mensagemErro,usuario=usuario)



#Para para entrar em contato com o ADMIN do site. Todas as mensagens enviadas sao salvas no BD
@app.route("/contatos")
def contatos():
    if "contatoCriado" in session:
        del session["contatoCriado"]
        return render_template("contatos.html",criacao=True)
    else:
        return render_template("contatos.html",criacao=False)



#Para com os dados sobre oque o site se propoe e o objetivo
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")



#Pagiina para criar uma conta no sistema
@app.route("/cadastrarse")
def cadastrarse():
    import json
    with open('app/assets/dados/cidades_e_estados.json') as file:
        cidades_e_estados = json.load(file)
        erro = False
        mensagemErro = None
        if 'erroCadastro' in session:
            erro = True
            mensagemErro = session["mensagemErroCadastro"]
            del session["erroCadastro"]
            del session["mensagemErroCadastro"]
        
        return render_template("cadastrarse.html",cidades_e_estados=cidades_e_estados,erro=erro,mensagemErro=mensagemErro)



#Para para iniciar uma sessao no sistema
@app.route("/entrar")
def entrar():
    if "parametrosEntrar" in session:
        nomeUsuario = session["parametrosEntrar"]["nomeUsuario"]
        acessoNegado = session["parametrosEntrar"]["acessoNegado"]
        mensagemErro = session["parametrosEntrar"]["mensagemErro"]
        del session["parametrosEntrar"]
        return render_template("entrar.html",acessoNegado=acessoNegado,nomeUsuario=nomeUsuario,mensagemErro=mensagemErro)
    else:
        return render_template("entrar.html",acessoNegado=False,nomeUsuario="")



#Pagina que mostrar os dados do usuario, como dados pessoais, formacao e experiencias
@app.route("/perfil/<usuario>")
def perfil(usuario):
    conn = bd.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario, email, estado, cidade, experiencia, formacao, aplicacoes, criacoes,dataNascimento, telefone, timestamp, genero, foto, nome FROM usuarios WHERE usuario = ?",(usuario,))
    dadosBD = cursor.fetchone()
    dados = bd.rowToDict(
        ['usuario','email','estado', 'cidade', 'experiencia', 'formacao', 'aplicacoes', 'criacoes', 'dataNascimento', 'telefone', 'timestamp','genero','foto','nome'],
        dadosBD
    )
    dados["formacao"] = json.loads(dados["formacao"])
    dados["experiencia"] = json.loads(dados["experiencia"])
    return render_template("perfil.html",dados=dados)



#Pagina que mostra as vagas criadas pelo usuario e as vagas em que ele se candidatou
@app.route("/minhasVagas")
def minhasVagas():

    #pegar as vagas criadas pelo usuario
    criacoes = bd.queryVagas("SELECT * FROM vagas WHERE usuario = ?;",(session["usuario"],))    
    for vaga in criacoes:
        aplicacoesOBJ = json.loads(vaga['aplicacoes'])
        qtdAprovados = 0
        qtdReprovados = 0
        qtdCandidatos = len(aplicacoesOBJ)
        for candidato in aplicacoesOBJ:
            if candidato["status"] == "aprovado":
                qtdAprovados += 1
            elif candidato["status"] == "reprovado":
                qtdReprovados += 1
        vaga["qtdAprovados"] = qtdAprovados
        vaga["qtdReprovados"] = qtdReprovados
        vaga["qtdCandidatos"] = qtdCandidatos

    #pegar as vagas em que o usuario se aplicou
    conn = bd.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT aplicacoes FROM usuarios WHERE usuario = ?",(session["usuario"],))
    dadosBD = cursor.fetchone()
    aplicacoes = json.loads(dadosBD[0])
    for aplicacao in aplicacoes:
        cursor.execute("SELECT titulo,salario,cidade,estado FROM vagas WHERE id = ?",(aplicacao["vaga"]))
        vaga = cursor.fetchone()
        aplicacao["titulo"] = vaga[0]
        aplicacao["salario"] = vaga[1]
        aplicacao["cidade"] = vaga[2]
        aplicacao["estado"] = vaga[3]
    
    return render_template("minhasVagas.html",criacoes=criacoes,aplicacoes=aplicacoes)



#Para para o usuario admin. Esta pagina mostra as mensagens enviadas na pagina contatos
@app.route("/admin")
def admin():
    if "usuario" in session:
        if session["usuario"] == "admin":
            contatos = bd.lerMensagem()
            return render_template("admin.html",contatos=contatos)
    
    return redirect(url_for("index"))