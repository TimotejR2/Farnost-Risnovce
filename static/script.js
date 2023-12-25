var mainElement;
var headerElement
// Open sidenav if screen widtch is more that 700
window.onload = function(){
  mainElement = document.getElementById('main');
  headerElement = document.getElementById("header");
    if (window.screen.availWidth > 700){
      openNav();
    }
}

document.addEventListener("DOMContentLoaded", function() {
  var links = document.querySelectorAll('.nav-link'); // Select all links
  
  links.forEach(function(link) {
      link.addEventListener('click', function(event) {
          removeActiveClass(); // Remove 'active' class from all links
          event.target.classList.add('active'); // Add 'active' class to the clicked link
      });
      
      var currentPath = window.location.pathname; // Get current path
      if (link.getAttribute('href') === currentPath) {
          link.classList.add('active'); // Add 'active' class to the link with the current path
      }
  });
});

function removeActiveClass() {
  var links = document.querySelectorAll('.nav-link'); // Select all links
  
  links.forEach(function(link) {
      link.classList.remove('active'); // Remove 'active' class from all links
  });
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


