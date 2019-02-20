$(document).ready(function() {

    $('#sidebar').toggleClass('active');

    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');
    });
});