 function like(post_id, user_id) {

        $.ajax({
            url: '/like/?post_id=' + post_id + '&user_id=' + user_id,
            type: 'POST',
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {

                if(JSON.parse(data).dislikes>=0){
                     $('#count-dislike').html(JSON.parse(data).dislikes);
                     $('#count-like').html(JSON.parse(data).likes);
                     $('#heart-like').css('color', JSON.parse(data).color);
                }
                if (JSON.parse(data).error) {
                    swal({title: '! خطا', text: JSON.parse(data).error, icon:'warning',type: "warning"}
                    ).then(function () {
                            window.location = "/login";

                        });
                }
                else {

                    $('#count-like').html(JSON.parse(data).likes)
                    $('#heart-like').css('color', JSON.parse(data).color);
                }

            }


        })
    }

function dislike(post_id, user_id) {

        $.ajax({
            url: '/dislike/?post_id=' + post_id + '&user_id=' + user_id,
            type: 'POST',
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if(JSON.parse(data).likes>=0){
                     $('#count-dislike').html(JSON.parse(data).dislikes);
                     $('#count-like').html(JSON.parse(data).likes);
                     $('#heart-like').css('color', JSON.parse(data).color);
                }
                if (JSON.parse(data).error) {
                    swal({title: '! خطا', text: JSON.parse(data).error, icon:'warning',type: "warning"}
                    ).then(function () {
                            window.location = "/login";

                        });
                } else {
                    $('#count-dislike').html(JSON.parse(data).dislikes);
                }

            }


        })
    }
