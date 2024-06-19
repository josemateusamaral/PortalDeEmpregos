import sqlite3
import json
import os
import random
from . import bcrypt


#coisas relacionadas com a estrutura do BD
def connect_to_db():
    if 'banco.db' not in os .listdir():
        try:
            with open("bancoBKP.db","rb") as file:
                with open("banco.db","wb") as banco:
                    banco.write(file.read())
        except: pass

    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vagas (
            id            INTEGER   PRIMARY KEY AUTOINCREMENT,
            titulo        TEXT      NOT NULL,
            cidade        TEXT      NOT NULL,
            descricao     TEXT      NOT NULL,
            requisitos    TEXT      NOT NULL,
            carga_horaria TEXT      NOT NULL,
            area          TEXT      NOT NULL,
            salario       TEXT      NOT NULL,
            aplicacoes    TEXT      NOT NULL,
            usuario       TEXT      NOT NULL,
            status        TEXT      NOT NULL,
            timestamp     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            modalidade    TEXT      NOT NULL,
            estado        TEXT      NOT NULL,
            tipo_contrato TEXT      NOT NULL
        );
    ''')
    conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL,
            email TEXT NOT NULL,
            estado TEXT NOT NULL,
            cidade TEXT NOT NULL,
            experiencia TEXT NOT NULL,
            formacao TEXT NOT NULL,
            aplicacoes TEXT NOT NULL,
            criacoes TEXT NOT NULL,
            dataNascimento TEXT NOT NULL,
            telefone TEXT NOT NULL,
            genero TEXT NOT NULL,
            foto TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            nome TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            mensagem TEXT NOT NULL
        );
    ''')

    conn.commit()
    return conn

def genRandKey20():
    key = ''
    chars = ['a','b','c','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for i in range(10):
        char = random.choice(chars)
        if random.choice([True,False]):
            char = char.upper()
        key += char
    return key

def rowToDict(cols,col):
    obj = {}
    for index,i in enumerate(cols):
        obj[i] = col[index]
    return obj





#coisas relacionadas ao usuario
def criarUsuario(formulario):

    #dados do novo usuario
    usuario = formulario["usuario"]
    email = formulario["email"]
    estado = formulario["estado"]
    cidade = formulario["cidade"]
    dataNascimento = formulario["dataNascimento"]
    telefone = formulario["telefone"]
    genero = formulario["genero"]
    nome = formulario["nome"]
    foto = "default.png"

    conn = connect_to_db()
    cursor = conn.cursor()

    #verificar se o usuario ja existe
    cursor.execute("SELECT usuario, email FROM usuarios WHERE usuario = ? OR email = ?",(usuario,email))
    retorno = cursor.fetchone()

    #usuario ja existe -> retornar erro
    if retorno != None:
        mensagemErro = None
        if usuario == retorno[0] and email == retorno[1]:
            mensagemErro = f"O usuário {usuario} e o email '{email}' já estão sendo usados"
        elif usuario == retorno[0]:
            mensagemErro = f"O usuário {usuario} já esta sendo usado"
        else:
            mensagemErro = f"O email {email} já esta sendo usado"
        return {"criado":False,"mensagemErro":mensagemErro}

    else:
        hashed_password = bcrypt.generate_password_hash(formulario['senha']).decode('utf-8')
        formacao = []
        experiencia = []
        aplicacoes = []
        criacoes = []
        cursor.execute(f"""
            INSERT INTO usuarios (usuario,senha,email,estado,cidade,formacao,experiencia,aplicacoes,criacoes,dataNascimento,telefone,genero,foto,nome) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        """,(usuario,hashed_password,email,estado,cidade,json.dumps(formacao),json.dumps(experiencia),json.dumps(aplicacoes),json.dumps(criacoes),dataNascimento,telefone,genero,foto,nome))
        conn.commit()
        conn.close()
        return {"criado":True}

def autenticarUsuario(formulario):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (formulario["usuario"],))
    conn.commit()
    senha = cursor.fetchone()
    conn.close()

    #usuario nao existe
    if not senha:
        return False

    #usuario autenticados
    if bcrypt.check_password_hash(senha[0], formulario["senha"]):
        return True    

    return False

def editarPerfil(request,usuario):

    print("editando>",request)

    formulario = request.form
    #dados do formulario
    nome = formulario["nome"]
    genero = formulario["genero"]
    cidade = formulario["cidade"]
    estado = formulario["estado"]
    telefone = formulario["telefone"]
    statusImagem = formulario["statusImagem"]
    dataNascimento = formulario["dataNascimento"]

    fotos = os.listdir('app/assets/data')
    foto = None
    while True:
        idFoto = usuario
        if idFoto not in fotos:
            imagem = request.files['imagem']
            imagem.save(f'app/assets/data/{idFoto}.jpg')
            foto = idFoto + '.jpg'
            break

    conn = connect_to_db()
    cursor = conn.cursor()
    if statusImagem == 'semImagem':
        cursor.execute("UPDATE usuarios SET nome = ?, genero = ?, cidade = ?, estado = ?, telefone = ?, dataNascimento = ? WHERE usuario = ?",(nome,genero,cidade,estado,telefone,dataNascimento,usuario))
    else:
        cursor.execute("UPDATE usuarios SET nome = ?, genero = ?, cidade = ?, estado = ?, telefone = ?, dataNascimento = ?, foto = ?, nome = ? WHERE usuario = ?",(nome,genero,cidade,estado,telefone,dataNascimento,foto,usuario,nome))
    conn.commit()
    conn.close()




#coisas relacionadas a vagas
def queryVagas(query,parametros=None):
    conn = connect_to_db()
    cursor = conn.cursor()
    if parametros == None:
        cursor.execute(query)
    else:
        cursor.execute(query,parametros)
    vagasBD = cursor.fetchall()
    vagasDict = []
    for vagaBD in vagasBD:
        vagasDict.append({'id':vagaBD[0],'titulo':vagaBD[1],'cidade':vagaBD[2],'descricao':vagaBD[3],'requisitos':vagaBD[4],'carga_horaria':vagaBD[5],'area':vagaBD[6],'salario':vagaBD[7],'aplicacoes':vagaBD[8],'usuario':vagaBD[9],'status':vagaBD[10],'timestamp':vagaBD[11],'modalidade':vagaBD[12],'estado':vagaBD[13],'tipo_contrato':vagaBD[14]})
    conn.close()
    return vagasDict

def queryVaga(id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, titulo, cidade, descricao, requisitos, carga_horaria, area, salario, aplicacoes, usuario, status, timestamp, modalidade, estado, tipo_contrato FROM vagas WHERE id = ?",(id))
    vagaBD = cursor.fetchall()
    vagaDict = {}
    if len(vagaBD) != 0:
        vagaBD = vagaBD[0]
        vagaDict = {'id':vagaBD[0],'titulo':vagaBD[1],'cidade':vagaBD[2],'descricao':vagaBD[3],'requisitos':vagaBD[4],'carga_horaria':vagaBD[5],'area':vagaBD[6],'salario':vagaBD[7],'aplicacoes':json.loads(vagaBD[8]),'usuario':vagaBD[9],'status':vagaBD[10],'data_postagem':vagaBD[11],'modalidade':vagaBD[12],'estado':vagaBD[13],'tipo_contrato':vagaBD[14]}
    conn.close()
    return vagaDict

def criarVaga(formulario,usuario):
    conn = connect_to_db()
    cursor = conn.cursor()
    aplicacoes = []
    cursor.execute(f"""
        INSERT INTO vagas(titulo,cidade,descricao,requisitos,carga_horaria,area,salario,modalidade,estado,tipo_contrato,aplicacoes,usuario,status) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);
    """,(formulario['titulo'],formulario['cidade'],formulario['descricao'],formulario['requisitos'],formulario['carga_horaria'],formulario['area'],formulario['salario'],formulario['modalidade'],formulario["estado"],formulario["tipo_contrato"],json.dumps(aplicacoes),usuario,"aberta"))
    id = cursor.lastrowid
    conn.commit()
    conn.close()
    return id

def editarVaga(formulario,usuario):
    conn = connect_to_db()
    cursor = conn.cursor()
    aplicacoes = []
    cursor.execute(f"""
        UPDATE vagas 
        SET titulo=?, cidade=?, descricao=?, requisitos=?, carga_horaria=?, area=? , salario=?, modalidade=?, estado=?, tipo_contrato=? 
        WHERE id = ? AND usuario = ? ;
    """,(formulario['titulo'],formulario['cidade'],formulario['descricao'],formulario['requisitos'],formulario['carga_horaria'],formulario['area'],formulario['salario'],formulario['modalidade'],formulario['estado'],formulario['tipo_contrato'],formulario["idVaga"],usuario))
    conn.commit()
    conn.close()
    return formulario["idVaga"]

def encerrarVaga(idVaga):
    vaga = queryVaga(idVaga)
    conn = connect_to_db()
    cursor = conn.cursor()
    
    for usuario in vaga["aplicacoes"]:
        if usuario["status"] != "aprovado":
            usuario["status"] = "reprovado"
            
            cursor.execute("SELECT aplicacoes FROM usuarios WHERE usuario = ?",(usuario["usuario"],))
            usuarioApli = cursor.fetchone()
            if usuarioApli != None:
                aplicacoes = json.loads(usuarioApli[0])
                for i in aplicacoes:
                    if i["vaga"] == idVaga:
                        aplicacoes.remove(i)
            cursor.execute("UPDATE usuarios SET aplicacoes = ? WHERE usuario = ?",(json.dumps(aplicacoes),usuario["usuario"]))

    vaga["status"] = "encerrada"
    cursor.execute("UPDATE vagas SET aplicacoes = ?, status = ? WHERE id = ?",(json.dumps(vaga["aplicacoes"]),vaga["status"],idVaga))

    conn.commit()
    conn.close()

def reabrirVaga(idVaga):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE vagas SET status = ? WHERE id = ?",("aberta",idVaga))
    conn.commit()
    conn.close()

def aplicarParaVaga(idVaga,usuario):
    aplicacaoObdUsuario = {"vaga":idVaga,"status":"analizando"}
    aplicacaoObdVaga = {"usuario":usuario,"status":"analizando"}

    #pegar a vaga
    vaga = queryVaga(idVaga)
    if vaga["usuario"] == usuario:
        return False

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT aplicacoes FROM usuarios WHERE usuario = ?",(usuario,))
    aplicacoesusuario = cursor.fetchone()
    if aplicacoesusuario == None:
        conn.commit()
        conn.close()
        return False
    else:

        #configurar aplicacao no usuario
        aplicacoesusuario = json.loads(aplicacoesusuario[0])
        if aplicacaoObdUsuario not in aplicacoesusuario:
            aplicacoesusuario.append(aplicacaoObdUsuario)
        aplicacoesBD = json.dumps(aplicacoesusuario)
        cursor.execute("UPDATE usuarios SET aplicacoes = ? WHERE usuario = ?",(aplicacoesBD,usuario))

        #configurar aplicacao na vaga
        cursor.execute("SELECT aplicacoes FROM vagas WHERE id = ?",(idVaga,))
        vaga = cursor.fetchone()
        if vaga != None:
            aplicacao = json.loads(vaga[0])
            if aplicacaoObdVaga not in aplicacao:
                aplicacao.append(aplicacaoObdVaga)
            aplicacao = json.dumps(aplicacao)
            cursor.execute("UPDATE vagas SET aplicacoes = ? WHERE id = ?",(aplicacao,idVaga))
            
        conn.commit()
        conn.close()
        return True

def cancelarAplicacao(idVaga,usuario):

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT aplicacoes FROM usuarios WHERE usuario = ?",(usuario,))
    aplicacoesusuario = cursor.fetchone()
    if aplicacoesusuario == None:
        conn.commit()
        conn.close()
        return False
    else:

        #configurar aplicacao no usuario
        aplicacoesusuario = json.loads(aplicacoesusuario[0])
        for i in aplicacoesusuario:
            if i["vaga"] == idVaga:
                aplicacoesusuario.remove(i)
        aplicacoesBD = json.dumps(aplicacoesusuario)
        cursor.execute("UPDATE usuarios SET aplicacoes = ? WHERE usuario = ?",(aplicacoesBD,usuario))

        #configurar aplicacao na vaga
        cursor.execute("SELECT aplicacoes FROM vagas WHERE id = ?",(idVaga,))
        vaga = cursor.fetchone()
        if vaga != None:
            aplicacao = json.loads(vaga[0])
            for i in aplicacao:
                if i["usuario"] == usuario:
                    aplicacao.remove(i)
            aplicacao = json.dumps(aplicacao)
            cursor.execute("UPDATE vagas SET aplicacoes = ? WHERE id = ?",(aplicacao,idVaga))
            
        conn.commit()
        conn.close()
        return True

def setEstatusCandidatura(idVaga,usuario,status):

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT aplicacoes FROM usuarios WHERE usuario = ?",(usuario,))
    aplicacoesusuario = cursor.fetchone()
    if aplicacoesusuario == None:
        conn.commit()
        conn.close()
        return False
    else:

        #configurar aplicacao no usuario
        aplicacoesusuario = json.loads(aplicacoesusuario[0])
        for i in aplicacoesusuario:
            if i["vaga"] == idVaga:
                i["status"] = status
        aplicacoesBD = json.dumps(aplicacoesusuario)
        cursor.execute("UPDATE usuarios SET aplicacoes = ? WHERE usuario = ?",(aplicacoesBD,usuario))

        #configurar aplicacao na vaga
        cursor.execute("SELECT aplicacoes FROM vagas WHERE id = ?",(idVaga,))
        vaga = cursor.fetchone()
        if vaga != None:
            aplicacao = json.loads(vaga[0])
            for i in aplicacao:
                if i["usuario"] == usuario:
                    i["status"] = status
            aplicacao = json.dumps(aplicacao)
            cursor.execute("UPDATE vagas SET aplicacoes = ? WHERE id = ?",(aplicacao,idVaga))
            
        conn.commit()
        conn.close()
        return True




#coisas relacionadas aos contatos
def criarContato(formulario):
    nome = formulario["nome"]
    email = formulario["email"]
    mensagem = formulario["mensagem"]

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contatos (nome,email,mensagem) VALUES (?,?,?)",(nome,email,mensagem))
    conn.commit()
    conn.close()

def lerMensagem():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos")
    conts = cursor.fetchall()
    conn.commit()
    conn.close()
    contatos = []
    for contato in conts:
        contatos.append({"id":contato[0],"nome":contato[1],"email":contato[2],"mensagem":contato[3]})

    return contatos

def apagarContato(formulario):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contatos WHERE id = ?",(formulario["id"],))
    conts = cursor.fetchall()
    conn.commit()
    conn.close()



#funcoes relacionadas a formacao
def criarFormacao(formulario,usuario):

    novaFormacao = {"id":genRandKey20()}
    for i in formulario:
        novaFormacao[i] = formulario[i]

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT formacao FROM usuarios WHERE usuario = ?",(usuario,))
    formacaousuario = cursor.fetchone()
    if formacaousuario == None:
        conn.commit()
        conn.close()
        return False
    else:
        formacaousuario = json.loads(formacaousuario[0])
        formacaousuario.append(novaFormacao)
        formacaoBD = json.dumps(formacaousuario)
        cursor.execute("UPDATE usuarios SET formacao = ? WHERE usuario = ?",(formacaoBD,usuario))
        conn.commit()
        conn.close()
        return True

def removerFormacao(formacao,usuario):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT formacao FROM usuarios WHERE usuario = ?",(usuario,))
    formacaousuario = cursor.fetchone()
    if formacaousuario == None:
        conn.commit()
        conn.close()
        return False
    else:
        formacaousuario = json.loads(formacaousuario[0])
        for formacaoBD in formacaousuario:
            if formacaoBD["id"] == formacao["id"]:
                formacaousuario.remove(formacaoBD)
        formacaoBD = json.dumps(formacaousuario)
        cursor.execute("UPDATE usuarios SET formacao = ? WHERE usuario = ?",(formacaoBD,usuario))
        conn.commit()
        conn.close()
        return True

def editarFormacao(formulario,usuario):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT formacao FROM usuarios WHERE usuario = ?",(usuario,))
    formacoes = json.loads(cursor.fetchone()[0])
    for formacao in formacoes:
        if formacao["id"] == formulario["id"]:
            formacao["titulo"] = formulario["titulo"]
            formacao["instituicao"] = formulario["instituicao"]
            formacao["duracao"] = formulario["duracao"]
            formacao["estado"] = formulario["estado"]
    novoFormacoes = json.dumps(formacoes)
    cursor.execute("UPDATE usuarios SET formacao = ? WHERE usuario = ?",(novoFormacoes,usuario))
    conn.commit()
    conn.close()



#Coisas relacionadas com as experiencias
def criarExperiencia(formulario,usuario):

    novaExperiencia = {"id":genRandKey20()}
    for i in formulario:
        novaExperiencia[i] = formulario[i]

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT experiencia FROM usuarios WHERE usuario = ?",(usuario,))
    experienciaUsuario = cursor.fetchone()
    if experienciaUsuario == None:
        conn.commit()
        conn.close()
        return False
    else:
        experienciaUsuario = json.loads(experienciaUsuario[0])
        experienciaUsuario.append(novaExperiencia)
        experienciaBD = json.dumps(experienciaUsuario)
        cursor.execute("UPDATE usuarios SET experiencia = ? WHERE usuario = ?",(experienciaBD,usuario))
        conn.commit()
        conn.close()
        return True

def removerExperiencia(experiencia,usuario):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT experiencia FROM usuarios WHERE usuario = ?",(usuario,))
    experienciausuario = cursor.fetchone()
    if experienciausuario == None:
        conn.commit()
        conn.close()
        return False
    else:
        experienciausuario = json.loads(experienciausuario[0])
        for experienciaBD in experienciausuario:
            if experienciaBD["id"] == experiencia["id"]:
                experienciausuario.remove(experienciaBD)
        experienciaBD = json.dumps(experienciausuario)
        cursor.execute("UPDATE usuarios SET experiencia = ? WHERE usuario = ?",(experienciaBD,usuario))
        conn.commit()
        conn.close()
        return True

def editarExperiencia(formulario,usuario):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT experiencia FROM usuarios WHERE usuario = ?",(usuario,))
    experiencias = json.loads(cursor.fetchone()[0])
    for experiencia in experiencias:
        if experiencia["id"] == formulario["id"]:
            experiencia["cargo"] = formulario["cargo"]
            experiencia["empresa"] = formulario["empresa"]
            experiencia["duracao"] = formulario["duracao"]
            experiencia["estado"] = formulario["estado"]
    novoExperiencias = json.dumps(experiencias)
    cursor.execute("UPDATE usuarios SET experiencia = ? WHERE usuario = ?",(novoExperiencias,usuario))
    conn.commit()
    conn.close()