
/* Abrir modal ao agendar */
document.getElementById("abrir-agendar").addEventListener("click", function(event){
    document.getElementById("modal").style.display = "block";
    // Garante que apenas o modal de agendamento dentro do iframe seja visível
    const iframeDoc = document.getElementById("iframe-modal").contentWindow.document;
    iframeDoc.getElementById("modal-agendando").style.display = "block";
});

/* Abrir modal ao editar */
document.getElementById("abrir-editar").addEventListener("click", function(event){
    document.getElementById("modal").style.display = "block";
    const iframeDoc = document.getElementById("iframe-modal").contentWindow.document;
    iframeDoc.getElementById("modal-editando").style.display = "block";
});

/* Abrir modal ao remover */
document.getElementById("abrir-remover").addEventListener("click", function(event){
    document.getElementById("modal").style.display = "block";
    const iframeDoc = document.getElementById("iframe-modal").contentWindow.document;
    iframeDoc.getElementById("modal-removendo").style.display = "block";
});

/* Abrir modal ao buscar */
document.getElementById("abrir-buscar").addEventListener("click", function(event){
    document.getElementById("modal").style.display = "block";
    const iframeDoc = document.getElementById("iframe-modal").contentWindow.document;
    iframeDoc.getElementById("modal-buscando").style.display = "block";
});

/* Fechar ao clicar fora do modal */
window.onclick = function(event){
    const modal = document.getElementById("modal");
    if(event.target == modal){
        modal.style.display = "none";
        
        // Esconde todos os painéis de conteúdo dentro do iframe
        const iframeDoc = document.getElementById("iframe-modal").contentWindow.document;
        iframeDoc.getElementById("modal-agendando").style.display = "none";
        iframeDoc.getElementById("modal-editando").style.display = "none";
        iframeDoc.getElementById("modal-removendo").style.display = "none";
        iframeDoc.getElementById("modal-buscando").style.display = "none";

        /* Deselecionar ao clicar fora */
        iframeDoc.querySelectorAll("#lista-compromisso li").forEach(function(el) {
            el.classList.remove("selecionado");
        });
    }
}


/* ================================================
 LÓGICA PARA MUDAR O TEMA (Refatorada com Classes CSS)
================================================
*/
const themeButton = document.getElementById("mudar");
const body = document.getElementById("body-index");

if (themeButton && body) {
    themeButton.addEventListener("click", function() {
        // Verifica qual tema está ativo e aplica o próximo, em ciclo
        if (body.classList.contains('theme-noite')) {
            // Estava no tema NOITE -> muda para TARDE
            body.classList.remove('theme-noite');
            body.classList.add('theme-tarde');
        } else if (body.classList.contains('theme-tarde')) {
            // Estava no tema TARDE -> muda para DIA (o padrão, sem classes extras)
            body.classList.remove('theme-tarde');
        } else {
            // Se não for nenhum dos dois (tema DIA) -> muda para NOITE
            body.classList.add('theme-noite');
        }
    });
}