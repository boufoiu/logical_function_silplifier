const loader = document.querySelector('.chargement');
const main = document.querySelector('.main2');
//Initialisation: Hiding the loader
loader.style.display = 'none';

// Affichage du résultat
document.getElementById("displayResultat").value=localStorage.getItem("shared_resultat");

// Synthèse
var syn = document.getElementById('syntheseres');
syn.addEventListener("click", () => {
    //Hiding the main and showing the loader
    main.style.display = 'none';
    loader.style.display = 'block';

    var res = localStorage.getItem("shared_resultat");

    // Before formatting:
    console.log("Before formatting:");
    console.log("res= " + res);

    // URL encoding:
    console.log("URL encoding:");
    res = encodeURIComponent(res); console.log(res);

    url = `http://127.0.0.1:8000/Synthese?formule=${res}`;

   // console.log(url);

    console.log("About to fetch the above url...");
    fetch(url)
    .then( ()=> {
        // Stop the load
        loader.style.display = "none";
        // Next page
        window.location="./synthese.html" ;  //Endpoint: /Frontend/synthese.html
    } )
        .catch(e => {
            console.log(e);
        });

})

// Etapes
var etp= document.getElementById("etapes");
etp.addEventListener("click", ()=> {

    if (localStorage.getItem("shared_resultat") == "FAUX"){
        alert("La fonction s'annule.\nAucune simplification n'est apportée");
    }
    else {
        // Next page
        window.location = "./etapes.html";
    }

})