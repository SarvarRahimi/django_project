function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(function () {
    $(".situation button").on("click", function (event) {
        event.preventDefault();
        let postId = $(".situation").attr('post-id');
        let typeChange = $(".situation").attr('type-change');
        let buttonId = $(this).attr('id');
        let buttonState = $(this).attr('button-state');
        const csrf_token = getCookie('csrftoken');
        let data = {
            "type_change": typeChange,
            "post_id": postId,
            "button_state": buttonState,
            "csrfmiddlewaretoken": csrf_token
        };

        $.ajax({
            headers: {'X-CSRFToken': csrf_token},
            url: ' http://127.0.0.1:8000/posting/changeActivation/',
            data: data,
            method: "POST",
        })
            .done(function (result) {
                alert("ثبت شد");
                if (result['status']) {
                    if (result['button'] === 'activation') {
                        $("#"+buttonId).addClass("btn-outline-success").removeClass("btn-outline-secondary").html('فعال');
                    } else {
                        $("#"+buttonId).addClass("btn-outline-success").removeClass("btn-outline-secondary").html('اجازه نمایش دارد');
                    }
                } else {
                    if (result['button'] === 'activation') {
                        $("#"+buttonId).addClass("btn-outline-secondary").removeClass("btn-outline-success").html('غیر فعال');
                    } else {
                        $("#"+buttonId).addClass("btn-outline-secondary").removeClass("btn-outline-success").html('اجازه نمایش ندارد');
                    }
                }
            })
            .fail(function (result) {
                alert("ثبت نشد" + result['status'] + result['exception']);
            });
    });
});