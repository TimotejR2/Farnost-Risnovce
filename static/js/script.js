// Initialize main and header elements
var mainElement
var headerElement

// Open sidenav if screen width is more than 700, get main and header elements
window.onload = function() {
  if (window.screen.availWidth > 700) {
    mainElement = document.getElementById('main');
    headerElement = document.getElementById("header");
    openNav();
  }
}

// Highlight active link based on current path
document.addEventListener("DOMContentLoaded", function() {
  var links = document.querySelectorAll('.nav-link'); // Select all links
  var currentPath = window.location.pathname; // Get current path\

  currentPath = currentPath.split('/').filter((_, index) => index < 2).join('/');
  console.log(currentPath)

  links.forEach(function(link) {
    var id = '/' + link.id;

    if (id === currentPath) {
      link.classList.add('active'); // Add 'active' class to the link with the current path
    }
  });
});

// Remove 'active' class from all links
function removeActiveClass() {
  var links = document.querySelectorAll('.nav-link');
  links.forEach(function(link) {
    link.classList.remove('active');
  });
}

// Open sidenav
function openNav() {
  document.getElementById("sidenav").style.width = "250px";
  mainElement.style.marginLeft = '250px';
  headerElement.style.visibility = "hidden";
  document.getElementById("header").style.maxHeight = '0';
}

// Close sidenav
function closeNav() {
  document.getElementById("sidenav").style.width = "0";
  mainElement.style.marginLeft = '0';
  headerElement.style.visibility = "visible";
  document.getElementById("header").style.maxHeight = '120px';
}

// Display submenu
function displayMenu(submenu) {
  document.getElementById(submenu).style.display = 'block';
}

// Hide submenu based on timeout
function hideMenu(submenu, menu) {
  setTimeout(function() {
    if (!document.querySelector(`#${submenu}:hover`) && !document.querySelector(`#${menu}:hover`)) {
      document.getElementById(submenu).style.display = 'none';
    }
  }, 100);
}

// Toggle menu visibility based on cursor support
let isMenuVisible = false;

function toggleMenu(menuId) {
  if (isCursorSupported()) {
    // Redirect to /menuId if cursor is supported
    menuId = menuId.replace('_submenu', '');

    if (menuId === 'domov') {
      menuId = '';
    }

    window.location.href = '/' + menuId;
  } else {
    // Toggle menu visibility for devices without cursor
    isMenuVisible ? hideMenu(menuId) : displayMenu(menuId);
    isMenuVisible = !isMenuVisible;
  }
}

// Check if the device supports a cursor (e.g., mouse)
function isCursorSupported() {
  return window.matchMedia('(pointer: fine)').matches;
}