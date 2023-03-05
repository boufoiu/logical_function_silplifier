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




          ///////////////////////////////////////////////////////











          ///////////////////////////////////////////////////
        }
        
        return valid; // return the valid status
      }    




      function inputStyleColor1(){
        document.getElementById("champ1").style.backgroundColor="#fffefeb8";
      }

      function inputStyleColor2(){
        document.getElementById("champ2").style.backgroundColor="#fffefeb8";
      }
      
      function inputStyleColor3(){
        document.getElementById("champ-rand-litr").style.backgroundColor="#fffefeb8";
      }

      function inputStyleColor4(){
        document.getElementById("champ-idtr").style.backgroundColor="#fffefeb8";
      }

      function inputStyleColor5(){
        document.getElementById("champ-var").style.backgroundColor="#fffefeb8";
      }

      function inputStyleColor6(){
        document.getElementById("champ-rand-num").style.backgroundColor="#fffefeb8";
      }



      function inputStyleColorImpliquantsTable(){

       var tab=document.getElementsByClassName("impliquant-important");//.style.backgroundColor="#fffefeb8";


       for(var i=0; i<tab.length;i++)
       {
        tab[i].style.backgroundColor="#fffefeb8";
       }


       
       
      
      }


  //  function exit(){
  //   var window=getElementById("exit");
  //     windows.on('click', function() {
  //       $(this).hide();
  //     });
  //  }


  //  exit();



  
  function closeWindow() {

      // Open the new window
      // with the URL replacing the
      // current page using the
      // _self value
      let new_window =
          open(location, '_self');

      // Close this window
      new_window.close();

      return false;
  }



  
   



     


      inputStyleColorImpliquantsTable();




//////////////////////////////

     


      



      function setFormuleSideIndicator(){
        // console.log("the value is " );
        let inputValue = document.getElementsByClassName('number')[0].value; 
        
        let new_value ='f( ';
        let i=1;
          
        if(inputValue<=4){
          
          for( i=1;i<inputValue;i++){
            new_value=new_value+String.fromCharCode(i+64) +'+';
          }
          new_value=new_value+ String.fromCharCode(i+64)+' ) =';
          
          
          
        }
        else if(inputValue>26){
          new_value='f(A1+..+A'+inputValue.toString() +' )=';
          
        }
        else if(4<inputValue<=26)
        {
          
          new_value='f(A+..+'+String.fromCharCode(parseInt(inputValue , 10)+64) +' )=';
        }
        document.getElementById("f-literale").innerHTML = new_value;
        
       
       
      }








      function passer_choix_forme()
      {
        if(validateForm()){
          
          var a = document.createElement("a");
             a.href="./choix_forme.html";

             a.click();
        }

            
      }

     



      