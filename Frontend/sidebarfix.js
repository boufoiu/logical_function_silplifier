
function setSideBarSizs()
{
    if(screen.width>1440){
        let Bar=document.getElementsByClassName('sidebar')[0];
        Bar.style.width="15.5%"
     }
     if(screen.width<1440){
         let Bar=document.getElementsByClassName('sidebar')[0];
         Bar.style.width="19%"
      }
}


setSideBarSizs();