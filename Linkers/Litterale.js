const loader= document.querySelector('.chargement');
const main= document.querySelector('.calc');
//Initialisation: Hiding the loader
loader.style.display = 'none';

// Afficher f(a,b..) jusqu'à la lettre correspondante au nombre de variable donné
function setFormuleSideIndicator() {
    // console.log("the value is " );
    let inputValue = localStorage.getItem("shared_nbvar");

    let new_value = 'f( ';
    let i = 1;

    if (inputValue <= 4) {

        for (i = 1; i < inputValue; i++) {
            new_value = new_value + String.fromCharCode(i + 64) + ',';
        }
        new_value = new_value + String.fromCharCode(i + 64) + ' ) =';

    }
    // else if (inputValue > 26) {
    //     new_value = 'f(A1+..+A' + inputValue.toString() + ' )=';
    // }
    else if (4 < inputValue <= 26) {

        new_value = 'f(A,B,..' + String.fromCharCode(parseInt(inputValue, 10) + 64) + ' )=';
    }
    document.getElementById("f-literale").innerHTML = new_value;
}

setFormuleSideIndicator();


var calculer = document.getElementById('calx');
calculer.addEventListener("click", () => {

    // Get user data
    var formule = document.getElementById('champ2').value;
    var nbvar = localStorage.getItem("shared_nbvar");

    // URL encoding:
    nbvar = encodeURIComponent(nbvar);
    formule = encodeURIComponent(formule);

    if (formule == "") { alert('Entrez une formule !!'); }
    else {
        //Hiding the main and showing the loader
        main.style.display = 'none';
        loader.style.display = 'block';

        url = `http://127.0.0.1:8000/SimplificationLitterale?nbVar=${nbvar}&formule=${formule}`;
        console.log("url="+url);
        console.log("About to fetch the above url...");
        fetch(url)
            .then( result => {
                return result.json()
            })      // Data returned is a dictionnary
            .then( data => {
                    //erreur syntaxique
                if (data.err == 1) {
                    main.style.display = 'block';
                    loader.style.display = 'none';
                    alert(data.resultat);    
                }   //formule simplifiée
                else{

                    // Storing data     
                    localStorage.setItem("shared_formule", data.resultat.resultat);
                    localStorage.setItem("shared_termesfct", data.resultat.fonction);
                    localStorage.setItem("shared_groupes", JSON.stringify (data.resultat.groupes) );
                    localStorage.setItem("shared_premiers", data.resultat.premiers);
                    localStorage.setItem("shared_essentiels", data.resultat.essentiels);   
                    // Stop the load
                    loader.style.display = "none";
                    // Next page
                    window.location = "./choix_forme.html";

                } 
            })
            .catch(e => {
                console.log(e);
            });
    }
});

var random = document.getElementById('rand');
random.addEventListener("click", () => {
    //document.getElementById("checkClick").innerHTML = "Button clicked !!";

    var nbvar = localStorage.getItem("shared_nbvar");
    var nbMin = document.getElementById('champ-rand-litr').value;

    // Before formatting:
    console.log("Before formatting:");
    console.log(nbvar);
    console.log(nbMin);

    // URL encoding:
    console.log("URL encoding:");
    nbvar = encodeURIComponent(nbvar); console.log(nbvar);
    nbMin = encodeURIComponent(nbMin); console.log(nbMin);

    if (nbMin == "") { alert("Entrez le nombre de minterme !! "); }
    else {

        url = `http://127.0.0.1:8000/RandomLitterale?nbVar=${nbvar}&nbmin=${nbMin}`;
        console.log(url);

        console.log("About to fetch the above url...");

        fetch(url)    //, body:{nbvar: nbvar }
            .then( (result) => {
                return result.json()
            })
            .then( (data) => {
                // Write the generated function in the input "formule"
                document.getElementById('champ2').value = data.randLit;

            })
            .catch(e => { console.log(e); });
    }
});