var adicionandoExperiencia = false;
var adicionandoFormacao = false;
var editandoExperiencia = false;
var editandoFormacao = false;

function toogleAdicionarFormacao(){

    if(adicionandoExperiencia){toogleAdicionarExperiencia()}
    if(editandoExperiencia){editarExperiencia()}
    if(editandoFormacao){editarFormacao()}

    let adicionar = document.getElementById("adicionarFormacao");
    let botao = document.getElementById("botaoToogleFormacao");
    if( adicionar.style.display == "none"){
        adicionandoFormacao = true;
        adicionar.style.display = "initial";
        botao.classList.add("d-none");
    }else{
        adicionandoFormacao = false;
        adicionar.style.display = "none";
        botao.innerText = "Adicionar";
        botao.classList.add("btn-primary");
        botao.classList.remove("btn-danger");
        botao.classList.remove("d-none");
    }
}

function editarFormacao(formacao){

    if(adicionandoExperiencia){toogleAdicionarExperiencia()}
    if(editandoExperiencia){editarExperiencia()}
    if(adicionandoFormacao){toogleAdicionarFormacao()}

    let editar = document.getElementById("editarFormacao");
    if( editar.style.display == "none"){
        editandoFormacao = true;
        editar.style.display = "initial";
        document.getElementById("idEditarFormacao").value = formacao.id;
        document.getElementById("tituloEditar").value = formacao.titulo;
        document.getElementById("instituicaoEditar").value = formacao.instituicao;
        document.getElementById("estadoEditar").value = formacao.estado;
        document.getElementById("duracaoEditar").value = formacao.duracao;
    }else{
        editandoFormacao = false;
        editar.style.display = "none";
    }
}

function toogleAdicionarExperiencia(){

    if(editandoFormacao){editarFormacao()}
    if(editandoExperiencia){editarExperiencia()}
    if(adicionandoFormacao){toogleAdicionarFormacao()}

    let adicionar = document.getElementById("adicionarExperiencia");
    let botao = document.getElementById("botaoToogleExperiencia");
    if( adicionar.style.display == "none"){
        adicionandoExperiencia = true;
        adicionar.style.display = "initial";
        botao.classList.add("d-none");
    }else{
        adicionandoExperiencia = false;
        adicionar.style.display = "none";
        botao.classList.remove("d-none");
    }
}


function editarExperiencia(experiencia){

    if(editandoFormacao){editarFormacao()}
    if(adicionandoExperiencia){toogleAdicionarExperiencia()}
    if(adicionandoFormacao){toogleAdicionarFormacao()}

    let editar = document.getElementById("editarExperiencia");
    if( editar.style.display == "none"){
        editandoExperiencia = true;
        editar.style.display = "initial";
        document.getElementById("idEditarExp").value = experiencia.id;
        document.getElementById("cargoEditar").value = experiencia.cargo;
        document.getElementById("empresaEditar").value = experiencia.empresa;
        document.getElementById("estadoExpEditar").value = experiencia.estado;
        document.getElementById("duracaoExpEditar").value = experiencia.duracao;
    }else{
        editandoExperiencia = false;
        editar.style.display = "none";
    }
}