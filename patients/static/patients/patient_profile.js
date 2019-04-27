$(document).ready(function () {


    $(".disabledBox").on("click", function (e) {
        console.log("EEK")
        var checkbox = $(this);
        // do the confirmation thing here

        e.preventDefault();
        $('#exampleModalCenter').modal('toggle');

        console.log(checkbox)
    });


});