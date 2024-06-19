
function configurarEstados() {
  let seletor = document.getElementById("estado");
  for (estado in cidades_e_estados) {
    seletor.innerHTML += `<option>${estado}</option>`;
  }
}

function atualizarMunicipios(selecao) {
  console.log("atualizando...");
  let estado = document.getElementById("estado").value;
  let seletorCidade = document.getElementById("cidade");
  seletorCidade.innerHTML = "<option selected disabled>Selecione sua cidade</option>";

  console.log("quantidade cidades:", cidades_e_estados[estado]["municipios"].length);
  for (cidade in cidades_e_estados[estado]["municipios"]) {
    let nomeCidade = cidades_e_estados[estado]["municipios"][cidade];
    if( nomeCidade == selecao ){
      seletorCidade.innerHTML += `<option selected>${nomeCidade}</option>`;
    }else{
      seletorCidade.innerHTML += `<option>${nomeCidade}</option>`;
    }
  }
  console.log(estado);
}

function __init__() {

    //ajustando o footer para ficar sempre no fim da página
    console.log('ajustando o footer...');
    var windowHeight = window.innerHeight;
    var windowWidth = window.innerWidth;
    var bodyHeight = document.body.clientHeight;
    var footer = document.querySelector('footer');
    if (windowHeight > bodyHeight) {
      footer.style.position = 'fixed';
      footer.style.bottom = '0';
      footer.style.width = '100%';
      console.log('footer fixado na parte de baixo da tela.')
    } else {
      footer.style.position = 'absolute';
      footer.style.width = '100%';
      console.log('footer fixado no fim do conteudo.');
    }
    window.onload = function() {
        __init__();
    };
    window.onresize = function() {
        __init__();
    };

}







