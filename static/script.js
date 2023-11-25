window.onload = function(){
    if (window.screen.availWidth > 700){
        document.getElementById("mySidenav").style.width = "250px";
    }
}

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}
