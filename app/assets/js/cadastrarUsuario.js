function submeterCadastro(){
    console.log('submetendo cadastro...');

    //dados do cadastro
    usuario = document.getElementById('usuario').value;
    senha1 = document.getElementById('senha1');
    senha2 = document.getElementById('senha2');

    if (senha1.value.indexOf(' ') !== -1){
        alert("A senha não pode conter espaços");
        return false;
    };

    //verificar se a senha e a repeticao estao iguais
    if( senha1.value != senha2.value ){
        alert("As senha não conferem. Para realizar o cadastro a senha e a senha repetida devem ser as mesmas !");
        return false;
    }

    // Verifica se o nome de usuário tem pelo menos 5 caracteres
    if (usuario.length < 5) {
        alert("O nome de usuário deve ter pelo menos 5 caracteres.");
        return false;
    }
  

    const hasFiveCaracters = senha1.value.length > 5;
    const hasUpperCase = /[A-Z]/.test(senha1.value); 
    const hasLowerCase = /[a-z]/.test(senha1.value);
    const hasNumbers = /[0-9]/.test(senha1.value);
    const hasSpecialCharacters = /[!@#$%^&*(),.?":{}|<>]/.test(senha1.value); 
    
    if( !hasFiveCaracters || !hasUpperCase || !hasLowerCase || !hasNumbers || !hasSpecialCharacters ){
        alert("A senha deve conter no minimo 6 caracteres sendo eles numeros, letras maiusculas, minusculas e caracteres.");
        return false;
    }

    //tudo certo. pode submeter o cadastro
    document.getElementById('formulario').submit();
    return true;
}

function isStrongPassword(password) {
    // Define os critérios da senha forte
    const minLength = 8; // comprimento mínimo
    const hasUpperCase = /[A-Z]/.test(password); // pelo menos uma letra maiúscula
    const hasLowerCase = /[a-z]/.test(password); // pelo menos uma letra minúscula
    const hasNumbers = /[0-9]/.test(password); // pelo menos um número
    const hasSpecialCharacters = /[!@#$%^&*(),.?":{}|<>]/.test(password); // pelo menos um caractere especial

    // Verifica se a senha atende a todos os critérios
    if (password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialCharacters) {
        return true; // A senha é forte
    } else {
        return false; // A senha não é forte
    }
  }