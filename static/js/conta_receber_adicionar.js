var banco = document.getElementById('banco');
var creditaCarteira = document.getElementById('creditaCarteira');
creditaCarteira.addEventListener('click',function(){
    if(this.checked){
        banco.disabled = true; 
        banco.removeAttribute("required");
    }else{
        banco.disabled = false;
        banco.setAttribute("required", "required");
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Obter a data de hoje no formato yyyy-mm-dd
    var today = new Date().toISOString().split('T')[0];
    
    // Atribuir a data de hoje ao atributo 'max' do campo de data
    document.getElementById("data_recebimento").max = today;
    
});