tag_list = []

$('#add-tag').click(function() {
    let div = $('<div class="row rounded mt-3" style="max-height: 100px;width: 100%"></div>').appendTo('#tags');
    let tag = $('<input type="text" class="rounded ml-3 mr-3" placeholder="نام تگ" required>').appendTo(div)
    $(tag).change(function() {
        tag_list.push($(tag).val())
    })
})

$('#newPost').click(function() {
    $('#all-tags').val(JSON.stringify(tag_list));
})
$('#edit').click(function() {
    $('#all-tags').val(JSON.stringify(tag_list));
})