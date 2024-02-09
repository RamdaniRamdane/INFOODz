document.addEventListener("DOMContentLoaded", function () {
    // Fonction pour mettre à jour la classe du lien de navigation actif
    function updateNavLinkClass() {
        // Récupère le chemin de la page actuelle
        var currentPage = window.location.pathname;
        console.log( currentPage);

        // Obtient les liens de navigation par leurs identifiants
        var homeLink = document.getElementById('home-link');
        var productsLink = document.getElementById('products-link');
        var alertsLink = document.getElementById('alerts-link');



        // Définir les liens actifs en fonction du chemin de la page actuelle
        if (currentPage === homeLink.getAttribute('href')) {
            homeLink.classList.add('current-page');
        } else {
            homeLink.classList.remove('current-page');
        }

        if (currentPage === productsLink.getAttribute('href')) {
            productsLink.classList.add('current-page');
        } else {
            productsLink.classList.remove('current-page');
        }

        if (currentPage === "/alerts/") {
            alertsLink.classList.add('current-page');


        } else {
            alertsLink.classList.remove('current-page');
        }
    }

    // Appelle la fonction au chargement initial de la page
    updateNavLinkClass();
});
