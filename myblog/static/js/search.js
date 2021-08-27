function search() {
    $.ajax({
        url: '/api/search/',
        type: 'POST',
        data: $('#search-input').val(),
        contentType: false,
        cache: false,
        processData: false,
        success: function(posts) {
            let data = JSON.parse(posts)
            console.log(data);
            if (data.error) {
                $('#search-posts').html('')
                let div = $(`<div class="row rounded mt-3 ml-4 alert alert-danger justify-content-center" style="width: 100%" >${data.error}</div>`).appendTo('#search-posts');
                setTimeout(function() {
                    $(div).fadeOut('slow');
                }, 2000);
            } else {
                $('#search-posts').html('')
                for (let post in data) {
                    let div = $('<div class="col-5 card rounded mt-3 ml-4" ></div>').appendTo('#search-posts');
                    let header = $('<div class="card-header justify-content-center"></div>').appendTo(div);
                    let img = $('<img class="rounded" style="height: auto;width: 100%">').appendTo(header);
                    $(img).attr('src', '/static/media/uploads/posts/' + `${data[post][1]}`)
                    let row = $('<div class=row justify-content-center></div>').appendTo(div)
                    let card_body = $('<div class="card-body"></div>').appendTo(row)
                    let button = $('<button type="button" ></button>').appendTo(card_body)
                    $(button).attr('class', 'btn btn-info');
                    let post_name = $('<a class="text-white" type="button" style="font-size: 15px"></a>').appendTo(button)
                    $(post_name).attr('href', '/post/' + `${post}/`);
                    $(post_name).html(`${data[post][0]}`);
                }


            }
        },
        error: function() {
            console.log('error')
        }


    })
}