// function timeSince(date) {
//     let pubDiv = document.getElementById("pubDate")
//
//     const seconds = Math.floor((new Date() - date) / 1000);
//
//     let interval = seconds / 31536000;
//
//     let result;
//     if (interval > 1) {
//         result = Math.floor(interval) + " سال قبل";
//         pubDiv.innerHTML = result;
//     }
//     interval = seconds / 2592000;
//     if (interval > 1) {
//         result = Math.floor(interval) + " ماه قبل";
//         pubDiv.innerHTML = result;
//     }
//     interval = seconds / 86400;
//     if (interval > 1) {
//         result = Math.floor(interval) + " روز قیل";
//         pubDiv.innerHTML = result;
//     }
//     interval = seconds / 3600;
//     if (interval > 1) {
//         result = Math.floor(interval) + " ساعت قبل";
//         pubDiv.innerHTML = result;
//     }
//     interval = seconds / 60;
//     if (interval > 1) {
//         result = Math.floor(interval) + " دقیقه قبل";
//         pubDiv.innerHTML = result;
//     }
//     else {
//         result = Math.floor(seconds) + " ثانیه قبل";
//         pubDiv.innerHTML = result;
//     }
// }


$(function () {
    $("#likeSvg").on("click",function (event) {
        event.preventDefault();
        let data = {
            "user_id": $(this).attr('user-id'),
            "post_id": $(this).attr('post-id'),
            "status": "True",
        };

        $.ajax({
            url: 'http://127.0.0.1:5000/order_final/',
            data: data,
            method: "POST",
        })
            .done(function (result) {
                alert("ثبت شد")
                $(this).css("color", "red");
                $(this).closest('p').html(result);
                // document.location = 'http://127.0.0.1:5000/';
            })
            .fail(function (result) {
                alert("ثبت نشد" + result['status'] + result['exception']);
            });
    });
});