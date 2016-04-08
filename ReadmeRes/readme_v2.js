$(document).ready(function() {
	$(".toplist").hide();
	$(".sublist").hide();

	$(".top_link").on("click", function(){
		if ($(this).parent().siblings(".toplist").is(':hidden')){
			$(this).parent().siblings(".toplist").show();
		}
		else {
			$(this).parent().siblings(".toplist").hide();
		}
	});
	$(".sub_link").on("click", function(){
		var q = '#' + $(this).attr('id');
		if ($(this).parent().siblings(q).is(':hidden')){
			$(this).parent().siblings(q).show();
		}
		else {
			$(this).parent().siblings(q).hide();
		}
	})
});

function click_slide(elem){
	
}