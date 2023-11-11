// Pour /calcule_rendement
const rendementForm = document.getElementById("rendementForm");
rendementForm.addEventListener("submit", function (e) {
    e.preventDefault();
    
    const formData = new FormData(rendementForm);
    
    fetch("/calcule_rendement", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("resultat").innerHTML = data;
    });
});

// Pour /calcule_valeur
const valeurForm = document.getElementById("valeurForm");
valeurForm.addEventListener("submit", function (e) {
    e.preventDefault();
    
    const formData = new FormData(valeurForm);
    
    fetch("/calcule_valeur", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("resultat").innerHTML = data;
    });
});

// Pour /calcule_rendement_totale
const rendementTotaleForm = document.getElementById("rendementTotaleForm");
rendementTotaleForm.addEventListener("submit", function (e) {
    e.preventDefault();
    
    const formData = new FormData(rendementTotaleForm);
    
    fetch("/calcule_rendement_totale", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("resultat").innerHTML = data;
    });
});
