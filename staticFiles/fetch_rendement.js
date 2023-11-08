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