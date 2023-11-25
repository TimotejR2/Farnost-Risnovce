var mainElement;
var headerElement
window.onload = function(){
  mainElement = document.getElementById('main');
  headerElement = document.getElementById("header");
    if (window.screen.availWidth > 700){
      openNav();
    }
}

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  mainElement.style.marginLeft = '250px';
  headerElement.style.visibility = "hidden";
  document.getElementById("header").style.maxHeight = '0';
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  mainElement.style.marginLeft = '0';
  headerElement.style.visibility = "visible";
  document.getElementById("header").style.maxHeight = '120px';
}


