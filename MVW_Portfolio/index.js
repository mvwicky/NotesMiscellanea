//var initValue = "Type name here";
var elems = ["Name", "Email", "GPA"];
var elemVals = elems;

//$(".Name input").attr("placeholder", initValue);

$(document).ready(function() {
  for (var i in elems) {
    var clElem = "." + elems[i];
    var dElem = "<div class= \"elem " + elems[i] + "\"> </div>";
    var initValue = "Type " + elems[i] + " here";
    $("body").append(dElem);
   
   $(clElem).append(" <input>");
   $(clElem).append(" <button>Click to add " + elems[i] + "</button>");
   $(clElem + " input").attr("placeholder", initValue);
   $(clElem + " button").addClass("new");
  }
  
  $(".elem button").on("click", function() {
    var elemType = $(this).parent().attr("class").slice(5);
    var p = elems.indexOf(elemType);
    elemVals[p] = $("." + elemType + " input").val();
    var elemSpan = "<span class=\"val\">" + elemVals[p] + " </span";
    $("." + elemType + " input").hide();

    $(this).parent().prepend(elemSpan);
    $(this).text("Edit " + elemType);
    $(this).removeClass("new");
    $(this).addClass("edit");
    
  });
  
});


  /*$(".Name button").on("click", function() {
    var name = $("div.Name input").val();
    var nameElem = "<span class=\"val\">" + name + " </span>";
    var isNew = $("div.Name button").hasClass("new");

    if (isNew == true) {
      $(".Name button").removeClass("new");
      $(".Name button").text("Edit Name");
      $(".Name input").remove();
      $(".Name").prepend(nameElem);
    }
    if (isNew == false) {
      $(".Name").find(".val").remove();
      $(".Name").prepend("<input>");
      $(".Name button").addClass("new");
      $(".Name button").text("Click to add name")
      $(".Name input").attr("placeholder", initValue);
    }
  });*/