$(document).ready(function () {


    $("#home").addClass("active");

    $("#home > a:nth-child(1)").attr("href", "#");


    let backwards = false;

    //Create function show_checked that grabs whether the checkboxes are checked or not, then only shows the checked catagories.
    //Might give a couple inputs later that allow it to be used on different checklists & different patient panels
    let show_checked = function () {

        //This should eventually be all columns
        let manipulated_columns = ['alerts-col', 'patients-col'];

        //On document ready, this would be an instance of, hence it should sort all columns, else, it should sort only the grandparent of the checkbox clicked's column(i.e patients-col, alerts-col)
        if (!(this instanceof Window)) {
            manipulated_columns = [$(this.parentNode.parentNode).attr('id')];
        }


        for (var j = 0; j < manipulated_columns.length; j++) {
            let checkList = $("#" + manipulated_columns[j] + " > label > input").get();


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
            let patient_statuses = $("#" + manipulated_columns[j] + " > div > a > small").get();


            //For all of the elements, set the display attr
            for (let i = 0; i < patient_statuses.length; i++) {
                if (patient_statuses[i].innerText === "Referred") {
                    patient_statuses[i].parentNode.style.display = referred;
                }
                if (patient_statuses[i].innerText === "In-Progress") {
                    patient_statuses[i].parentNode.style.display = inprogress;
                }
                if (patient_statuses[i].innerText === "Ready") {
                    patient_statuses[i].parentNode.style.display = ready;
                }
                if (patient_statuses[i].innerText === "Done") {
                    patient_statuses[i].parentNode.style.display = done;
                }
            }
        }

    };

    //Call the function on document ready because checkbox check status is cached when page is refreshed
    show_checked();


    //Apply the function as a listener to the checkboxes themselves
    $(".main-col > label > input").change(show_checked);

    let sort_list_group = function (event) {

        //Comparator function between a's text and b's text
        let sort_by_last_name = function (a, b) {
            return a.innerHTML.localeCompare(b.innerHTML, {sensitivity: 'base'});
        };

        let sort_by_first_name = function (a, b) {
            return a.innerHTML.substring(a.innerHTML.indexOf(',') + 1).localeCompare(b.innerHTML.substring(b.innerHTML.indexOf(',') + 1));
        };


        let columnToBeSorted = $(this.parentNode.parentNode.parentNode).attr('id');
        //Lists of patients names
        let list = $("#" + columnToBeSorted + " > div > a > div > h5").get();


        if (event.data.sort_method === "last") {
            list = list.sort(sort_by_last_name);
        } else if (event.data.sort_method === "first") {
            list = list.sort(sort_by_first_name)
        }

        if (!false) {
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

    };
    //Sort the patients by first name
    $(".main-col > div > div > .sortByFirst").click({sort_method: "first"}, sort_list_group);
    //Sort the patients by last name
    $(".main-col > div > div > .sortByLast").click({sort_method: "last"}, sort_list_group);


});