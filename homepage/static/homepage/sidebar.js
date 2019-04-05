time = new Date().getHours();
    username = $('#greeting').text()
    $('#greeting').text("");
    greeting = "";

    if(time >=3 && time < 12){
        greeting = "Good morning, ";
    } else if(time >=12 && time < 18){
        greeting = "Good afternoon, ";
    } else{
        greeting = "Good evening, "
    }

$(document).ready(function () {



    $('#greeting').text(greeting + username);



    $("#sidebar").mCustomScrollbar({
         theme: "minimal"
    });

    $('#sidebarCollapse').on('click', function () {
        // open or close navbar
        $('#sidebar, #content').toggleClass('active');
        // close dropdowns
        $('.collapse.in').toggleClass('in');
    });

    //To disable the analytics for the meanwhile
    $("#analytics > a:nth-child(1)").attr("href", "#");
});