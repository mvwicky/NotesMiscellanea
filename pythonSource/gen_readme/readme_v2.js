$(document).ready(function() {
	$(".toplist").hide();
	$(".sublist").hide();

	$(".top_link").on("click", function(){
		if ($(this).parent().siblings(".toplist").is(':hidden')){
			$(this).parent().siblings(".toplist").show("fast");
			$(this).siblings(".arrow").removeClass('arrow_right');
			$(this).siblings(".arrow").addClass('arrow_down');
		}
		else {
			$(this).parent().siblings(".toplist").hide("fast");
			$(this).siblings(".arrow").addClass('arrow_right');
			$(this).siblings(".arrow").removeClass('arrow_down');
		}
	});
	$(".arrow").on("click", function(){
		if ($(this).parent().siblings(".toplist").is(':hidden')){
			$(this).parent().siblings(".toplist").show("fast");
			$(this).removeClass('arrow_right');
			$(this).addClass('arrow_down');
		}
		else {
			$(this).parent().siblings(".toplist").hide("fast");
			$(this).addClass('arrow_right');
			$(this).removeClass('arrow_down');
		}
	});
	$(".sub_link").on("click", function(){
		var sub = '#' + $(this).attr('id');
		if ($(this).parent().siblings(sub).is(':hidden')){
			$(this).parent().siblings(sub).show("fast");
		}
		else {
			$(this).parent().siblings(sub).hide("fast");
		}
	})
});

function click_slide(elem){
	
}