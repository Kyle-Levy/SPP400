$(document).ready(function () {


    $(".modalCheckbox").on("click", function (e) {
        var checkboxClicked = $(this).children()[0];

        console.log(checkboxClicked.id)
        e.preventDefault();

        $('#' + checkboxClicked.id +'Modal').modal('toggle');

    });


});