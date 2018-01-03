
$(document).ready(function() {
    // JQuery code to be added in here.

    $("#about-btn").click( function(event) {
            alert("You clicked the button using JQuery!");
    });

    $("#about-btn").addClass('btn btn-warning');

    /*$("p").hover( function() {
        $(this).css('color', 'red');
    },
    function() {
        $(this).css('color', 'black');
    }); */

    $("#about-btn").click( function(event) {
        msgstr = $("#msg").html()
        msgstr = msgstr + "oo"
        $("#msg").html(msgstr)
    });

});
