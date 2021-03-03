$(function () {
    $(".labelBtn").on("click", function (event) {
        event.preventDefault();
        let labelVal = $("#labelBoxInput").val();
        $('<option>'+ labelVal +'</option>').appendTo('.labelsBox');
        $("#labelBoxInput").val('')
    });
});