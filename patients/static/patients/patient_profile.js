$(document).ready(function () {


    $(".modalCheckbox").on("click", function (e) {
        var checkboxClicked = $(this).children()[0];

        e.preventDefault();

        $('#' + checkboxClicked.id +'Modal').modal('toggle');

    });

    $(".modalCheckButton").on("click", function(e){
        console.log("EEEK");
       var checkButtonID = e.target.id;
       var checkboxID = checkButtonID.substring(0,3);

       console.log(checkboxID);
       var checkbox_element = $('#' + checkboxID);

       console.log(checkbox_element);
       if(checkbox_element.prop("checked") === true){
           checkbox_element.prop("checked", false);
       } else {
           checkbox_element.prop("checked", true);
       }

        $(this).parent().parent().parent().parent().modal('toggle');
    });


});