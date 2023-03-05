const loader = document.querySelector('.chargement');
const main = document.querySelector('.mainchoix');
//Initialisation: Hiding the loader
loader.style.display = 'none';


//En cliquant sur forme disjonctive
var disj = document.getElementById('disjonctive');
disj.addEventListener("click", () => {
    //Hiding the main and showing the loader
    main.style.display = 'none';
    loader.style.display = 'block';
    
    var res = localStorage.getItem("shared_formule");

    // URL encoding:
    res = encodeURIComponent(res);

    url = `http://127.0.0.1:8000/FormeResultat?formule=${res}&forme=DNF`;

    fetch(url)
        .then(result => {
            return result.json()
        })      // Data returned is a dictionnary
        .then(data => {
            localStorage.setItem("shared_resultat", data.formeRes)
            // Stop the load
            loader.style.display = "none";
            // Next page
            window.location = "./Resulatat.html"
        })
        .catch(e => {
            console.log(e);
        });
})

//En cliquant sur forme conjonctive
var conj = document.getElementById('conjonctive');
conj.addEventListener("click", () => {
    //Hiding the main and showing the loader
    main.style.display = 'none';
    loader.style.display = 'block';

    var res = localStorage.getItem("shared_formule");

    // URL encoding:
    res = encodeURIComponent(res);

    url = `http://127.0.0.1:8000/FormeResultat?formule=${res}&forme=CNF`;

    fetch(url)
        .then(result => {
            return result.json()
        })      // Data returned is a dictionnary
        .then(data => {
            localStorage.setItem("shared_resultat", data.formeRes)
            // Stop the load
            loader.style.display = "none";
            // Next page
            window.location = "./Resulatat.html"
        })
        .catch(e => {
            console.log(e);
        });
    
})