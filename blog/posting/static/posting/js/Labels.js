$(function () {
    $(".labelBtn").on("click", function (event) {
        event.preventDefault();
        let labelVal = $("#labelBoxInput").val();
        $('<p>'+ labelVal +'</p>').appendTo('.labelsBox');
        $("#labelBoxInput").val('')
    });
});