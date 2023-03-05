//verif
//setFormuleSideIndicator()

function validateForm() {
    // This function deals with validation of the form fields
    var y, i, valid = true;

    y = document.getElementsByTagName("input");

    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {

        // If a field is empty...
        if ((y[i].value == "") && (y[i].className == "number")) {


            y[i].style.backgroundColor = "#ffdddd";
            // and set the current valid status to false
            valid = false;
            // y[i].value == "";

            let new_value = "Champ vide";
            document.getElementById("message_erreur_litr").innerHTML = new_value;


        }
        if ((parseInt(y[i].value, 10) > 26) && y[i].className == "number") {
            y[i].style.backgroundColor = "#ffdddd";
            // and set the current valid status to false
            valid = false;

            let new_value = "Veuillez donner une valeur inferieure a 26";
            document.getElementById("message_erreur_litr").innerHTML = new_value;
        }


        if ((parseInt(y[i].value, 10) < 1) && y[i].className == "number") {
            y[i].style.backgroundColor = "#ffdddd";
            // and set the current valid status to false
            valid = false;

            let new_value = "Valeur non valide";
            document.getElementById("message_erreur_litr").innerHTML = new_value;
        }
    }

    return valid; // return the valid status
}

document.getElementById("suivant").addEventListener("click", () => {

    var verif= validateForm();
    if (verif==true){

        localStorage.setItem("shared_nbvar", document.getElementById("champ1").value);
        var a = document.createElement("a");
        a.href = "../Frontend/Litterale.html";
        a.click();

        
    }

});