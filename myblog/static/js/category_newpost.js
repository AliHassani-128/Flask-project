$(".btn_category").click(function (){
  $("#category_content").toggle()
})
$(".cat_btn").click(function(){
  var data=$(this).val()
  $("#select_category").val(data)
})

$(".select_c").click(function (){
  $("#category_content").hide();
$('#label').show()})