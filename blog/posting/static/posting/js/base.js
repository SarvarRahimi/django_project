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
    $(".postLikes div svg").on("click", function (event) {
        event.preventDefault();
        const csrf_token = getCookie('csrftoken');
        let data = {
            "user_id": $(this).attr('user-id'),
            "post_id": $(this).attr('post-id'),
            "status": $(this).attr('status'),
            "csrfmiddlewaretoken": csrf_token
        };

        $.ajax({
            headers: {'X-CSRFToken': csrf_token},
            url: ' http://127.0.0.1:8000/posting/postLiking/',
            data: data,
            method: "POST",
        })
            .done(function (result) {
                alert("ثبت شد");
                if (result['status']) {
                    $('#likePost').html(result['count']);
                } else {
                    $('#dislikePost').html(result['count']);
                }
            })
            .fail(function (result) {
                alert("ثبت نشد" + result['status'] + result['exception']);
            });
    });

    $(".commentLikes div svg").on("click", function (e) {
        e.preventDefault();
        const csrf_token = getCookie('csrftoken');
        let data = {
            "user_id": $(this).attr('user-id'),
            "comment_id": $(this).attr('comment-id'),
            "status": $(this).attr('status'),
            "csrfmiddlewaretoken": csrf_token
        };

        $.ajax({
            headers: {'X-CSRFToken': csrf_token},
            url: ' http://127.0.0.1:8000/posting/commentLiking/',
            data: data,
            method: "POST",
        })
            .done(function (result) {
                alert("ثبت شد");
                if (result['status']) {
                    $('#likeComment').html(result['count']);
                } else {
                    $('#dislikeComment').html(result['count']);
                }
            })
            .fail(function (result) {
                alert("ثبت نشد" + result['status'] + result['exception']);
            });

    });
});