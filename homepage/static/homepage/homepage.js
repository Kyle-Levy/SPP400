$(document).ready(function () {


    $("#home").addClass("active");

    $("#home > a:nth-child(1)").attr("href", "#");

    var backwards = false;

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