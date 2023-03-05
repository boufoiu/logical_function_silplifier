const loader = document.querySelector('.chargement');
const main = document.querySelector('.main');
//Initialisation: Hiding the loader
loader.style.display = 'none';

//Definir la fonction
function VerifNum (copy_formule){
    const error = [];
    if (copy_formule != ''){
        // var formule = Array.from(copy_formule);
        var formule = copy_formule.split("");
        const virgule = [];
        // Traitement du début
        if (formule[0] == ',' || isNaN(parseInt(formule[0])) ){
            if (formule[0] != ' ') {
                error.push(1);
                virgule[0] = true;
            }
        }
        // Traitement du milieu
        var num = 0;
        for (var i = 1; i < formule.length; i++) {
            if ((formule[i] != " ") && (formule[i] != ",")) {
                num = parseInt(formule[i]);
                if ( isNaN(num) ) {
                    error.push(i+1);
                }
                if (formule[i] != " " ) {
                    virgule.push(false);
                }

            }
            else if (formule[i] == ",") {
                virgule.push(true);
                if (virgule[virgule.length - 2] == true) {
                    error.push(i+1);
                }
            }

        }
        // Traitement de la fin
        if (formule[i - 1] == ',') {
            error.push(i);
        }
        
    }
    return error;

}

var calculer = document.getElementById('calx');
calculer.addEventListener("click", () => {

    // Get user data
    var formule = document.getElementById('champ2').value;
    var indet = document.getElementById('champ-idtr').value;


    if (formule == "") { alert('Entrez une formule'); }
    else {

        console.log("formule= " + formule);
        console.log("indet= " + indet);

        //Verification syntaxique de la formule
        var errors = VerifNum(formule);
        if (errors.length != 0){
            alert("ERREUR dans formule!! Caractère non autorisé aux positions "+ errors.toString());
        }
        else {
            //Verification syntaxique de l'indeterminée
            var errors = VerifNum(indet);
            console.log(errors);
            if (errors.length != 0) {
                alert("ERREUR dans l'indeterminée!! Caractère non autorisé aux positions " + errors.toString());
            }
            else {
                // URL encoding:
                indet = encodeURIComponent(indet);
                formule = encodeURIComponent(formule);

                //Hiding the main and showing the loader
                main.style.display = 'none';
                loader.style.display = 'block';

                url = `http://127.0.0.1:8000/SimplificationNumerique?exp=${formule}`;

                // Ajouter les indeterminées si elles existent, sinon = Null
                if (indet != "") { url += `&indet=${indet}`; }

                console.log("About to fetch the above url...");
                fetch(url)
                    .then((result) => {
                        return result.json()
                    })
                    .then((data) => {
                        // Storing data
                        localStorage.setItem("shared_formule", data.resultat);
                        localStorage.setItem("shared_termesfct", data.fonction);
                        localStorage.setItem("shared_groupes", JSON.stringify(data.groupes));
                        localStorage.setItem("shared_premiers", data.premiers);
                        localStorage.setItem("shared_essentiels", data.essentiels);
                        // Stop the load
                        loader.style.display = "none";
                        // Next page
                        window.location="./choix_forme.html"    
                    })
                    .catch(e => { console.error(e); });
            }
        }
 
    }
});

var random = document.getElementById('rand');
random.addEventListener("click", () => {
 
    var nbvar = document.getElementById('champ-var').value;
    var nbMin = document.getElementById('champ-rand-num').value;

    // Before formatting:
    console.log("Before formatting:");
    console.log(nbvar);
    console.log(nbMin);



    if (nbvar == "") { alert("Entrez le nombre de variable !! "); } 
    else {
        if (nbMin == "") { alert("Entrez le nombre de minterme !! "); }
        else {  
            if (nbMin >= (2 ** nbvar)) { alert("Entrez un nombre < " + (2 ** nbvar)); }  
            else {
                url = `http://127.0.0.1:8000/RandomNumerique?debut=0&fin=${(2 ** nbvar) - 1}&nbMin=${nbMin}`;

                console.log(url);

                console.log("About to fetch the above url...");

                fetch(url)    //, body:{nbvar: nbvar }
                    .then((result) => {
                        console.log(result)
                        return result.json()
                    })
                    .then((data) => {
                        // Write the generated function in the input "formule"
                        console.log("data: " + data);
                        console.log("formuleNum: " + data.randNum);

                        document.getElementById('champ2').value = (data.randNum);
                    })
                    .catch(e => { console.log(e); });

            }  
        }

    }
});

