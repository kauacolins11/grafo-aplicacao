document.addEventListener("DOMContentLoaded", function () {
    const selected = document.querySelector(".selected");
    const optionsContainer = document.querySelector(".options");
    const optionsList = document.querySelectorAll(".option");
    const generoInput = document.getElementById("genero");

    selected.addEventListener("click", () => {
        optionsContainer.classList.toggle("show");
    });

    optionsList.forEach(option => {
        option.addEventListener("click", () => {
            selected.innerText = option.innerText; // Atualiza o texto selecionado
            generoInput.value = option.getAttribute("data-value"); // Define o valor oculto
            optionsContainer.classList.remove("show"); // Fecha a lista de opções
        });
    });

    // Fecha a lista de opções ao clicar fora dela
    window.addEventListener("click", (e) => {
        if (!selected.contains(e.target) && !optionsContainer.contains(e.target)) {
            optionsContainer.classList.remove("show");
        }
    });
});