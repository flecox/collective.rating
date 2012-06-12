function collectiveRatingRate(starCls) {
  var stars = $(starCls);
  stars.addClass("star");
  stars.hover(function() {
    var star = $(this);
    var prev = star.prev();
    while(prev.length && prev.hasClass("star")) {
      prev.addClass("star-hover");
      prev = prev.prev();
    }
  },function() {
      $(".star-hover").removeClass("star-hover");
  });
  stars.click(function(e) {
    e.preventDefault();
    var star = $(this);
    var url = star.attr("href");
    $.ajax({
      url: url,
      dataType: 'json',
      data: {'rate_from':'ajax'},
      success: function(result, status) {
          if(status === "success") {
            var clickedStar = $($(starCls)[result['number']-1]);
            var prev = clickedStar.prev();
            var next = clickedStar.next();
            while(prev.length && prev.hasClass("star")) {
              prev.addClass("star-clicked");
              prev = prev.prev();
            }
            while(next.length && next.hasClass("star")) {
              next.removeClass("star-clicked");
              next.removeClass("star-rated");
              next.addClass("star-not-rated");
              next = next.next();
            }
            clickedStar.addClass("star-clicked");
        }
      }
    });
    return false;
  })
}