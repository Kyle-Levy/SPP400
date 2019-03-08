$(document).ready(function () {


    $("#home").addClass("active");

    $("#home > a:nth-child(1)").attr("href", "#");


    let backwards = false;

    //Create function show_checked that grabs whether the checkboxes are checked or not, then only shows the checked catagories.
    //Might give a couple inputs later that allow it to be used on different checklists & different patient panels
    let show_checked = function () {
        let checkList = $("#patients-col > label > input").get();

        //Default values for checks
        let referred = "none";
        let inprogress = "none";
        let ready = "none";
        let done = "none";

        //If checked, the elements should be displayed so display attribute is empty
        if (checkList[0].checked) {
            referred = "";
        }

        if (checkList[1].checked) {
            inprogress = "";
        }

        if (checkList[2].checked) {
            ready = "";
        }

        if (checkList[3].checked) {
            done = "";
        }

        //Get all of the 'statuses' of the patients in the list group
        let patient_statuses = $("a > small").get();


        //For all of the elements, set the display attr
        for (let i = 0; i < patient_statuses.length; i++) {
            if (patient_statuses[i].innerHTML === "Referred") {
                patient_statuses[i].parentNode.style.display = referred;
            }
            if (patient_statuses[i].innerHTML === "In-Progress") {
                patient_statuses[i].parentNode.style.display = inprogress;
            }
            if (patient_statuses[i].innerHTML === "Ready") {
                patient_statuses[i].parentNode.style.display = ready;
            }
            if (patient_statuses[i].innerHTML === "Done") {
                patient_statuses[i].parentNode.style.display = done;
            }
        }


    };

    //Call the function on document ready because checkbox check status is cached when page is refreshed
    show_checked();

    //Apply the function as a listener to the checkboxes themselves
    $("#patients-col > label > input").change(show_checked);

    let sort_list_group = function () {

        //Comparator function between a's text and b's text
        let sort_by_last_name = function (a, b) {
            return a.innerHTML.localeCompare(b.innerHTML, {sensitivity: 'base'});
        };

        let sort_by_first_name = function (a, b) {
            return a.innerHTML.substring(a.innerHTML.indexOf(',') + 1).localeCompare(b.innerHTML.substring(b.innerHTML.indexOf(',') + 1));
        };

        let list = $("a > div > h5").get();

        list = list.sort(sort_by_last_name);


        if (!backwards) {
            for (let i = 0; i < list.length; i++) {
                //list-group.append <a> of list[i]
                list[i].parentNode.parentNode.parentNode.append(list[i].parentNode.parentNode);
            }
        } else if (backwards) {
            for (let i = 0; i < list.length; i++) {
                //list-group.append <a> of list[i]
                list[i].parentNode.parentNode.parentNode.prepend(list[i].parentNode.parentNode);
            }
        }
        backwards = !backwards;

    }
    //Sort the patients by last name
    $("#sortAll").click(sort_list_group);


});