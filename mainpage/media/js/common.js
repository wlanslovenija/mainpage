(function($){
  $.fn.addAnchor = function(title) {
    title = title || _("Link here");
    return this.filter("*[id]").each(function() {
      $("<a class='anchor'> \u00B6</a>").attr("href", "#" + this.id).attr("title", title).appendTo(this);
    });
  }
})(jQuery);

jQuery(document).ready(function($) {
  $("#content").find("h1,h2,h3,h4,h5,h6").addAnchor("Link to this section");
  $("#content").find(".wikianchor").each(function() {
    $(this).addAnchor("Link to " + $(this).attr('id'));
  });
});
