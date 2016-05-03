$(document).ready(function() {
  var i = 0;
  $('.table.med').not('.h1').each(function(index, elem) {
    $(elem).find('*').addClass('med')
  });
  $('.table.wide').not('.h1').each(function(index, elem) {
    $(elem).find('*').addClass('wide')
  });
  $('.table > .trow').each(function(index, elem) {
    if ($(elem).children().hasClass('thead')) {
      i = 0;
      return true;
    }
    if (i % 2 == 0)
      $(elem).addClass('odd');
    else
      $(elem).addClass('even');
    i++;
  });

});
