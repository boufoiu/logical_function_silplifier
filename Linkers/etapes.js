// Liste des impliquants premiers
document.getElementById("impliq_premier").innerHTML = localStorage.getItem("shared_premiers");
 
// Liste des impliquants premiers essentiels
document.getElementById("impliq_ess").innerHTML = localStorage.getItem("shared_essentiels");



/* -------------------------------------- */
/*             TABLE DES GROUPES          */
/* ----------------------------------- -- */

// Récupération des données
var listegroupes =  JSON.parse(localStorage.getItem("shared_groupes"));

// Création du tableau
var table = document.getElementById("groupes-table");
table.border = '1';

var i = 0;
for (var k=0; k< listegroupes.length; k++ ) {
    var groupe = listegroupes[k];
    if (groupe.liste.length == 0) {
        var row = table.insertRow(i);
        var grpindex = row.insertCell(0);
        grpindex.innerHTML = ("Groupe " + k );
        var impliqindex = row.insertCell(1);
        impliqindex.innerHTML = "Liste vide";
        i++;
    }
    else {
        for (var j = 0; j < groupe["liste"].length; j++) {
            var row = table.insertRow(i);
            if (j == 0) {
                var grpindex = row.insertCell(0);
                grpindex.innerHTML = ("Groupe " + k );
                grpindex.rowSpan = groupe.liste.length;
                var impliqindex = row.insertCell(1);
            }
            else {
                var impliqindex = row.insertCell(0);
            }
            impliqindex.innerHTML = groupe.liste[j];
            i++;
        }
    }

}

// Ajout de l'entête
var header = table.createTHead();
var row = header.insertRow(0);



// row.insertCell(0).innerHTML = "Groupes";
// row.insertCell(1).innerHTML = "Liste des termes";


var cell1 = document.createElement("th");
var cellText1 = document.createTextNode("Groupes");
cell1.appendChild(cellText1);
row.appendChild(cell1);

var cell2 = document.createElement("th");
var cellText2 = document.createTextNode("Liste des termes");
cell2.appendChild(cellText2);
row.appendChild(cell2);




/* -------------------------------------- */
/*           TABLE DES IMPLIQUANTS        */
/* ----------------------------------- -- */

// Récupération des données
var listeTermes = localStorage.getItem("shared_termesfct").split(",");
var listeImpliq = localStorage.getItem("shared_premiers").split(",");


// Retourne vrai si l'impliquant (impliq) peut représenter le minterme (terme)
function contient(impliq, terme) {
    //Convert string to array
    impliq = Array.from(impliq);
    terme = Array.from(terme);

    var fin = false;
    while (!fin) {
        if (impliq.includes("-")) {
            var i = impliq.indexOf("-");
            impliq.splice(i, 1);
            terme.splice(i, 1);
        }
        else {
            fin = true;
        }
    }
    //Convert array to string
    impliq = impliq.join('');
    terme = terme.join('');
    if (impliq == terme) { return true; }
    else { return false; }
}

var table2 = document.getElementById("impliquants-essentiels-table");
table2.border = '1';

// Création du tableau
for (var i = 0; i < listeImpliq.length; i++) {
    var row = table2.insertRow(i);
    var impliq= row.insertCell(0);
    impliq.innerHTML = listeImpliq[i];
    // Si l'impliquant est essentiel => le désigner par une colour
    if (localStorage.getItem("shared_essentiels").split(",").includes(listeImpliq[i]) ) {

        impliq.style.color = "red";  
        impliq.style.color="#85ebd9";
      impliq.style.borderColor = "#85ebd9";
        impliq.style.backgroundColor="#3D898D";
        impliq.style.borderStyle="dashed";
  
    }

    // Test si impliq contient chaque terme
    for (var j = 0; j < listeTermes.length; j++) {
        var cell = row.insertCell(j + 1);

        if (contient(listeImpliq[i], listeTermes[j]) ){
            cell.innerHTML = "\u272D";
            cell.style.color="#85ebd9";
            // cell.style.borderColor="#85ebd9";
            cell.style.backgroundColor="#3D898D";
            // cell.style.borderStyle="dashed";
        }

    }
}

// Ajout de l'entête
var header = table2.createTHead();
var row = header.insertRow(0);


var cell1 = document.createElement("th");
var cellText1 = document.createTextNode("Impliquants \\ Termes");
cell1.appendChild(cellText1);
row.appendChild(cell1);


// row.insertCell(0).innerHTML = "Impliquants \\ Termes";
for (i=0; i<listeTermes.length; i++){

        var cell1 = document.createElement("th");
        var cellText1 = document.createTextNode(listeTermes[i]);
       
        cell1.appendChild(cellText1);
        row.appendChild(cell1);


    // row.insertCell(i+1).innerHTML = listeTermes[i];
}




/////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////


const multiStepForm = document.querySelector("[data-multi-step]")
const formSteps = [...multiStepForm.querySelectorAll("[data-step]")]
let currentStep = formSteps.findIndex(step => {
  return step.classList.contains("active")
})

if (currentStep < 0) {
  currentStep = 0
  showCurrentStep()
}

multiStepForm.addEventListener("click", e => {
  let incrementor
  if (e.target.matches("[data-next]") && validateForm() ) {
    if (validateForm()) {
      
    }
    incrementor = 1
    
  } else if (e.target.matches("[data-previous]") ) {
    incrementor = -1
  }

  if (incrementor == null) return

  const inputs = [...formSteps[currentStep].querySelectorAll("input")]
  const allValid = inputs.every(input => input.reportValidity())

  if (allValid && ((e.target.matches("[data-next]") && validateForm() )  || e.target.matches("[data-previous]")) ) {
    
  // if (e.target.matches("[data-previous]")) {
    

  //   var empt1,empt2;
  //   empt1 = formSteps[currentStep].getElementsByTagName("input");

  //       for (i = 0; i < empt1.length; i++) {
  //         empt1[i].value = ("");
          
            
  //         }

  //    empt2 = formSteps[currentStep].getElementsByTagName("textarea");

  //       for (i = 0; i < empt2.length; i++) {
  //         empt2[i].value = ("");
          
            
  //         }


  // }
    


    
    currentStep += incrementor

    showCurrentStep()
  }
  else if(e.target.matches("[data-next]") && !validateForm()){
    
  }
})

formSteps.forEach(step => {
  step.addEventListener("animationend", e => {
    formSteps[currentStep].classList.remove("hide")
    e.target.classList.toggle("hide", !e.target.classList.contains("active"))
  })
})

function showCurrentStep() {
  formSteps.forEach((step, index) => {
    step.classList.toggle("active", index === currentStep)
  })
} 


var loader=document.getElementById("wellcome");
    window.addEventListener("load",function()
    {
      setTimeout(function(){ loader.style.display="none"; }, 3000);

      
    }
    )


function validateForm() {
        // This function deals with validation of the form fields
        var y, i, valid = true;
        
        y = formSteps[currentStep].getElementsByTagName("input"); 
        
        // A loop that checks every input field in the current tab:
        for (i = 0; i < y.length; i++) {
          
          // If a field is empty...
          if ((y[i].value == "")  && (y[i].className=="input-fonction" || y[i].className=="res" || y[i].className=="number")) {
            
           
            y[i].style.backgroundColor="#ffdddd";
            // and set the current valid status to false
            valid = false;
           // y[i].value == "";

           let new_value="Champ vide";
            document.getElementById("message_erreur_litr").innerHTML = new_value;


          }
          if ((parseInt(y[i].value , 10)>26)&& y[i].className=="number") {
            y[i].style.backgroundColor="#ffdddd";
            // and set the current valid status to false
            valid = false;

            let new_value="Veuillez donner une valeur inferieure a 26";
            document.getElementById("message_erreur_litr").innerHTML = new_value;
          }


          if ((parseInt(y[i].value , 10)<1)&& y[i].className=="number") {
            y[i].style.backgroundColor="#ffdddd";
            // and set the current valid status to false
            valid = false;

            let new_value="Valeur non valide";
            document.getElementById("message_erreur_litr").innerHTML = new_value;
          }
        }
        
        return valid; // return the valid status
      }    


/////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////