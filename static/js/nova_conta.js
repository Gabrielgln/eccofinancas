var categoria = document.getElementById('categoria');

categoria.addEventListener('change', function(){
    var numero_parcela = document.getElementById('numero_parcela');
    var numero_parcela_paga = document.getElementById('numero_parcela_paga');
    var valor_total = document.getElementById('valor_total');
    var data_vencimento = document.getElementById('data_vencimento');
    var conta_debitar = document.getElementById('conta_debitar');

    categoriaOpcao = categoria.value;
    if(categoriaOpcao == 1){
        console.log(numero_parcela)
        numero_parcela.disabled = true;
        numero_parcela.removeAttribute("required");
        numero_parcela_paga.disabled = true;
        numero_parcela_paga.removeAttribute("required");
        valor_total.disabled = true;
        valor_total.removeAttribute("required");
        data_vencimento.disabled = true;
        data_vencimento.removeAttribute("required");
        conta_debitar.disabled = true;
        conta_debitar.removeAttribute("required");
    }
    else{
        numero_parcela.disabled = false;
        numero_parcela.setAttribute("required", "required");
        numero_parcela_paga.disabled = false;
        numero_parcela_paga.setAttribute("required", "required");
        valor_total.disabled = false;
        valor_total.setAttribute("required", "required");
        data_vencimento.disabled = false;
        data_vencimento.setAttribute("required", "required");
        conta_debitar.disabled = false;
        conta_debitar.setAttribute("required", "required");
    };
})

var debitaCarteira = document.getElementById('debitaCarteira');
debitaCarteira.addEventListener('click',function(){
    if(this.checked){
        conta_debitar.disabled = true; 
        conta_debitar.removeAttribute("required");
    }else{
        conta_debitar.disabled = false;
        conta_debitar.setAttribute("required", "required");
    }
});

