function delete_post(post_id) {

    swal({
        title: "اخطار حذف پست",
        text: "آیا مطمئن هستید می خواهید پست را حذف کنید؟",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#de3030",
        confirmButtonText: "بله",
        cancelButtonText: "بازگشت",
        closeOnConfirm: false,
        closeOnCancel: false,
        dangerMode: true,

    }).then(function(isConfirm) {
            if (isConfirm) {
                $.ajax({
                    url: "/api/delete-post/" + post_id,
                    type: 'GET',
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function () {
                        swal({
                            title: "حذف پست",
                            text: "پست شما با موفقیت حذف شد",
                            type: "success",icon:'success'
                        }).then(function () {
                            window.location = "/";

                        });

                    }


                })

            }

        })


}


function post_deactive(post_id) {

    $.ajax({
        url: "/api/post-deactive/" + post_id,
        type: 'GET',
        contentType: false,
        cache: false,
        processData: false,
        success: function () {

            swal({
                title: '! غیرفعال کردن پست',
                text: 'پست شما با موفقیت غیر فعال شد',
                type: 'success',
                icon:'success',
            }).then(function () {
                window.location = "/";

            });
        }


    })


}

function post_active(post_id) {

    $.ajax({
        url: "/api/post-active/" + post_id,
        type: 'GET',
        contentType: false,
        cache: false,
        processData: false,
        success: function () {
            swal({
                title: ' فعال کردن پست',
                text: 'پست شما با موفقیت فعال شد',
                type: 'success',
                icon:'success',
            }).then(function () {

                window.location = "/";

            });
        }


    })


}


