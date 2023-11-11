$(document).ready(function() {
      var mc = {
        'negative': 'red',
        'positive': 'green'
      };

      function getColorClass(x) {
        return x < 0 ? 'negative' : 'positive';
      }

      $('td').each(function(index) {
        var td = $(this);
        var dc = parseInt($(this).attr('data-color'), 10);
        var colorClass = getColorClass(dc);
        td.addClass(mc[colorClass]);
      });
    });