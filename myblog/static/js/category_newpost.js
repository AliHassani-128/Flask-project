var toggler = document.getElementsByClassName("caret");

for (let i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}
$(".cat_btn").click(function(){
  var data=$(this).val()
  $("#select_category").val(data)
  console.log(JSON.stringify(data))
    console.log($("#select_category").val())
      console.log(typeof ($("#select_category").val()))





})