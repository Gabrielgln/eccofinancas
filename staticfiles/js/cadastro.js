class Validator {

    constructor() {
        this.validations = [
            'data-required',
            'data-min-length',
            'data-max-length',
            'data-email-validate',
            'data-only-letters',
            'data-equal',
            'data-password-validate'
        ]
    }
    //iniciar a validação de todos os campos
    validate(form){
        var currentValidations = document.querySelectorAll('form .error-validation');
        //pega todos, se já tiver, ele limpa e valida dnv
        if(currentValidations.length > 0){
            this.cleanValidations(currentValidations);
            console.log(currentValidations);
        }

        var inputs = form.getElementsByTagName("input");

        //transformo htmlcollection -> array
        var inputsArray = [...inputs];
        //loop dos inputs e validação mediante ao que for encontrado
        inputsArray.forEach(function(input){
            for(var i = 0; this.validations.length > i;i++){
                //verifica se a validação atual existe no input
                if(input.getAttribute(this.validations[i]) != null){
                    //deixando "data-min-length" para "minlength"
                    var method = this.validations[i].replace('data-','').replace('-','');
                    //valor do atributo que foi passado no html exemplo data-min-length='3'
                    var value = input.getAttribute(this.validations[i]);
                    //invocar o metodo
                    this[method](input, value);
                }
            }
        },this);
    }

    minlength(input, minValue) {
        var inputLength = input.value.length;
        var errorMessage = `O campo precisa ter pelo menos ${minValue} caracteres`;

        if(inputLength < minValue){
            this.printMessage(input, errorMessage);
        }
    }

    maxlength(input, maxValue){
        var inputLength = input.value.length;
        var errorMessage = `O campo precisa ter no máximo ${maxValue} caracteres`;

        if(inputLength > maxValue){
            this.printMessage(input, errorMessage);
        }
    }

    required(input){
        var inputValue = input.value;
        if(inputValue == ""){
            var errorMessage = `Este campo é obrigatório`;

            this.printMessage(input, errorMessage);
        }
    }
    //valida email
    emailvalidate(input) {
        var re = /\S+@\S+\.\S+/;

        var email = input.value;

        var errorMessage = `Insira um e-mail valido`;
        //se não for um e-mail
        if(!re.test(email)){
            this.printMessage(input, errorMessage);
        }
    }
    //valida se o campo tem apenas letras
    onlyletters(input){
        var re = /^[A-Za-z]+$/;

        var inputValue = input.value;

        var errorMessage = `Este campo não aceita números nem caracteres especiais`;
        if(!re.test(inputValue)){
            this.printMessage(input, errorMessage);
        }
    }
    //verifica se dois campos são iguais
    equal(input, inputName){
        //0 por que é o primeiro e unico
        var inputToCompare = document.getElementsByName(inputName)[0];
        
        var errorMessage = `Este campo precisa estar igual ao ${inputName}`;

        if(input.value != inputToCompare.value){
            this.printMessage(input, errorMessage);
        }
    }
    //valida campo de senha
    passwordvalidate(input){
        var charArr = input.value.split("");

        var uppercases = 0;
        var numbers = 0;

        for(let i = 0; charArr.length > i;i++){
            if(charArr[i] == charArr[i].toUpperCase() && isNaN(parseInt(charArr[i]))){
                uppercases = uppercases + 1;
            }
            else if(!isNaN(parseInt(charArr[i]))){
                numbers = numbers + 1;
            }
        }
        if(uppercases == 0 || numbers == 0){
            var errorMessage = `A senha precisa de um caractere maiúsculo e um número`;
            this.printMessage(input, errorMessage);
        }
    }

    //metodo para imprimir mensagens de erro na tela
    printMessage(input, msg){
        var errorQte = input.parentNode.querySelector('.error-validation');
        //para não imprimir varios erros por cima do outro
        if(errorQte == null){
            var template = document.querySelector('.error-validation').cloneNode(true);

            template.textContent = msg;
            var inputParent = input.parentNode;
            
            template.classList.remove('template');
        
            inputParent.appendChild(template)
        } 
    }
    //limpa as validações da tela
    cleanValidations(validations){
        validations.forEach(element => element.remove());
    }

    validateCheckbox(){
        var checkbox = document.getElementById('agreement');
        var template = document.querySelector('.error-validationTwo').cloneNode(true);
        var currentValidations = document.querySelectorAll('form .error-validationTwo');
        if(currentValidations.length > 0){
            validator.cleanValidations(currentValidations);
        }
        if(!checkbox.checked){
            template.textContent = `Este campo é obrigatório`;
            template.classList.remove('template');
            checkbox.parentNode.appendChild(template);
        }
    }

    VerificateAll(){
        var currentValidations = document.querySelectorAll('.error-validation');
        var currentValidationsTwo = document.querySelectorAll('.error-validationTwo');
        var countValidation = currentValidations.length + currentValidationsTwo.length;
        //2 por conta que tem dois paragrafos criados no html
        if(countValidation == 2){
            form.submit();
            // alert("Você foi cadastrado com sucesso");
            // this.cleanInputs();
        }
    }

    cleanInputs(){
        var inputs = document.getElementsByTagName("input");
        for (var i = 0; i < inputs.length; i++) {
            console.log(inputs[i].type)
            if(inputs[i].type != "submit"){
                inputs[i].value = "";
            }
            if(inputs[i].type === "checkbox"){
                inputs[i].checked = false;
            }
        }
    }
}
var form = document.getElementById("register-form");
var submit = document.getElementById("btn-submit");

var validator = new Validator();

// evento que dispara as validações
submit.addEventListener("click", function(event){
    event.preventDefault();
    validator.validate(form);
    validator.validateCheckbox();
    validator.VerificateAll();
})