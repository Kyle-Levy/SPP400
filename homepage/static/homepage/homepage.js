$(document).ready(function () {


    $("#home").addClass("active");

    $("#home > a:nth-child(1)").attr("href", "#");


    var backwards = false;
    $('#testeroonie').text("TEST GOOD");

    
    var show_checked = function () {
        var checkList = $("#patients-col > label > input").get();

        var referred = "none";
        var inprogress = "none";
        var ready = "none";
        var done = "none";

        if(checkList[0].checked){
            referred = "";
        }

        if(checkList[1].checked){
            inprogress = "";
        }

        if(checkList[2].checked){
            ready = "";
        }

        if(checkList[3].checked){
            done = "";
        }

        patient_statuses = $("a > small").get();

        console.log(patient_statuses);

        for(var i = 0; i < patient_statuses.length; i++){
            if(patient_statuses[i].innerHTML == "Referred"){
                patient_statuses[i].parentNode.style.display = referred;
            }
            if(patient_statuses[i].innerHTML == "In-Progress"){
                patient_statuses[i].parentNode.style.display = inprogress;
            }
            if(patient_statuses[i].innerHTML == "Ready"){
                patient_statuses[i].parentNode.style.display = ready;
            }
            if(patient_statuses[i].innerHTML == "Done"){
                patient_statuses[i].parentNode.style.display = done;
            }
        }

        console.log(document.getElementById("kylelevy").style.display);



    }

    show_checked();

    $("#patients-col > label > input").change(show_checked);

    $("#sortAll").click(function () {
        var sort_by_last_name = function (a, b) {
            return a.innerHTML.toLowerCase().localeCompare(b.innerHTML.toLowerCase());
        }

        console.log(backwards);

        var list = $("a > div > h5").get();

        list = list.sort(sort_by_last_name);


        if (!backwards) {
            for (var i = 0; i < list.length; i++) {
                //list-group.append <a> of list[i]
                list[i].parentNode.parentNode.parentNode.append(list[i].parentNode.parentNode);
            }
        }
        else if(backwards){
            for (var i = 0; i < list.length; i++) {
                //list-group.append <a> of list[i]
                list[i].parentNode.parentNode.parentNode.prepend(list[i].parentNode.parentNode);
            }
        }
        backwards = !backwards;

    });



});