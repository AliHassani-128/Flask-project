$(".btn_category").click(function (){
  $("#category_content").toggle()
})
$(".cat_btn").click(function(){
  var data=$(this).val()
  $("#select_category").val(data)
  console.log(JSON.stringify(data))
    console.log($("#select_category").val())
      console.log(typeof ($("#select_category").val()))
})

$(".select_category").click(function (){
  $("#category_content").hide()})
