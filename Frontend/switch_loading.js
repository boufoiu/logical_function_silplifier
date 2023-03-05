let passage=true; //variable globale qui determine si on passe a la page rsulatt ou pas
//elle doit etre changer par le calucule une foit le calcul tremine

function passer_au_resultat()
{
if(passage)
{
var a = document.createElement("a");
a.href="./Resulatat.html";

a.click();
}



}


setTimeout(passer_au_resultat, 1500); //cette ligne de code sera retirer apres le link car cest just pour voir linterface