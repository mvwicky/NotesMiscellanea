$(document).ready(function() {
	$(".subone ul").hide();

	$(".subone a").on("click", function(){
		console.log($(this).parent().siblings());
		if ($(this).parent().siblings("ul").is(':hidden')){
			$(this).parent().siblings("ul").show();
		}
		else {
			$(this).parent().siblings("ul").hide();
		}
	});
});