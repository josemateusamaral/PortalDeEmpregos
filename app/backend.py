from flask import request,render_template,session,redirect,url_for,flash
from . import bd
from . import app
import os



# rotas relacionadas com acesso ao sistema
@app.route("/processo/cadastrarse",methods=['POST'])
def processocadastrarse():
    usuario = request.form["usuario"]
    criacao = bd.criarUsuario(request.form)
    if criacao["criado"]:
        session["usuario"] = usuario
        if "aplicacaoPendente" in session:
            vaga = session["aplicacaoPendente"]
            del session["aplicacaoPendente"]
            bd.aplicarParaVaga(vaga,session["usuario"])
            return redirect(f'/vaga/{vaga}')
        else:
            return redirect(f'/perfil/{session["usuario"]}')
    else:
        session["erroCadastro"] = True
        session["mensagemErroCadastro"] = criacao["mensagemErro"]
        return redirect(f'/cadastrarse')

@app.route("/processo/entrar",methods=['POST'])
def processoEntrar():
    if not bd.autenticarUsuario(request.form):
        session["parametrosEntrar"] = {"acessoNegado":True,"nomeUsuario":request.form["usuario"],"mensagemErro":"Credenciais de acesso inválidas. Tente novamente"}
        return redirect(url_for("entrar"))
    else:
        session['usuario'] = request.form['usuario']
        if "aplicacaoPendente" in session:
            vaga = session["aplicacaoPendente"]
            del session["aplicacaoPendente"]
            bd.aplicarParaVaga(vaga,session["usuario"])
            return redirect(f'/vaga/{vaga}')
        else:
            return redirect(url_for('index'))

@app.route("/processo/sair")
def processoSair():
    if 'usuario' in session:
        del session['usuario']
    return redirect(url_for('index'))



#rotas relacionadas com o gerenciamento de vagas
@app.route("/processo/reprovarCandidato",methods=['POST'])
def processoReprovarCandidato():
    idVaga = request.form["idVaga"]
    usuario = request.form["usuario"]
    bd.setEstatusCandidatura(idVaga,usuario,"reprovado")
    return redirect(url_for('minhasVagas'))

@app.route("/processo/aprovarCandidato",methods=['POST'])
def processoAprovarCandidato():
    idVaga = request.form["idVaga"]
    usuario = request.form["usuario"]
    bd.setEstatusCandidatura(idVaga,usuario,"aprovado")
    return redirect(url_for('minhasVagas'))

@app.route("/processo/analizarCandidato",methods=['POST'])
def processoAnalizarCandidato():
    idVaga = request.form["idVaga"]
    usuario = request.form["usuario"]
    bd.setEstatusCandidatura(idVaga,usuario,"analizando")
    return redirect(url_for('minhasVagas'))

@app.route("/processo/encerrarVaga",methods=['POST'])
def processoEncerrarVaga():
    idVaga = request.form["idVaga"]
    bd.encerrarVaga(idVaga)
    return redirect(url_for('minhasVagas'))

@app.route("/processo/reabrirVaga",methods=['POST'])
def processoReabrirVaga():
    idVaga = request.form["idVaga"]
    bd.reabrirVaga(idVaga)
    return redirect(url_for('minhasVagas'))

@app.route("/processo/criar",methods=['POST'])
def processoCriar():
    id = bd.criarVaga(request.form,session["usuario"])
    return redirect(url_for(f'vaga',idVaga=id))

@app.route("/processo/editar",methods=['POST'])
def processoEditar():
    id = bd.editarVaga(request.form,session["usuario"])
    return redirect(url_for(f'vaga',idVaga=id))
    
@app.route("/processo/aplicarParaVaga",methods=['POST'])
def processoAplicarParaVaga():
    if "usuario" in session:
        bd.aplicarParaVaga(request.form["idVaga"],session["usuario"])
        return redirect(url_for("minhasVagas"))
    else:
        session["parametrosEntrar"] = {"acessoNegado":True,"nomeUsuario":"","mensagemErro":"Para poder se aplicar a uma vaga, você precisa estar logado em alguma conta."}
        session["aplicacaoPendente"] = request.form["idVaga"]
        return redirect(url_for('entrar'))

@app.route("/processo/cancelarAplicacao",methods=['POST'])
def processoCancelarAplicacao():
    bd.cancelarAplicacao(request.form["idVaga"],session["usuario"])
    return redirect(url_for("minhasVagas"))



# rotas relacionadas com o gerenciamento de perfil
@app.route("/processo/editarPerfil",methods=['POST'])
def processoEditarPerfil():
    bd.editarPerfil(request,session["usuario"])
    return redirect(url_for(f'perfil',usuario=session["usuario"]))

@app.route("/processo/adicionarExperiencia",methods=['POST'])
def processoAdicionarExperiencia():
    bd.criarExperiencia(request.form,session["usuario"])
    return redirect(url_for(f'perfil',usuario=session["usuario"]))

@app.route("/processo/removerExperiencia",methods=['POST'])
def processoRemoverExperiencia():
    bd.removerExperiencia(request.form,session["usuario"])
    return redirect(url_for(f'perfil',usuario=session["usuario"]))

@app.route("/processo/editarExperiencia",methods=['POST'])
def processoEditarExperiencia():
    bd.editarExperiencia(request.form,session["usuario"])
    return redirect(url_for(f'perfil',usuario=session["usuario"]))

@app.route("/processo/adicionarFormacao",methods=['POST'])
def processoAdicionarFormacao():
    bd.criarFormacao(request.form,session["usuario"])
    return redirect(url_for(f'perfil',usuario=session["usuario"]))

@app.route("/processo/removerFormacao",methods=['POST'])
def processoRemoverFormacao():
    bd.removerFormacao(request.form,session["usuario"])
    return redirect(url_for(f'perfil',usuario=session["usuario"]))

@app.route("/processo/editarFormacao",methods=['POST'])
def processoEditarFormacao():
    bd.editarFormacao(request.form,session["usuario"])
    return redirect(url_for(f'perfil',usuario=session["usuario"]))



#coisas relacionadas com ADMIN
@app.route("/processo/contato",methods=['POST'])
def processoContato():
    bd.criarContato(request.form)
    session["contatoCriado"] = True
    return redirect(url_for(f'contatos'))

@app.route("/processo/apagarContato",methods=['POST'])
def processoApagarContato():
    bd.apagarContato(request.form)
    return redirect(url_for(f'admin'))