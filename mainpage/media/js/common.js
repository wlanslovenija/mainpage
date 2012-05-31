(function($){
    $.fn.addAnchor = function(title) {
        title = title || _("Link here");
        return this.filter('*[id]').each(function() {
            $('<a class="anchor"> \u00B6</a>').attr('href', '#' + this.id).attr('title', title).appendTo(this);
        });
    }
})(jQuery);

jQuery(document).ready(function($) {
    $('#content').find('h1,h2,h3,h4,h5,h6').addAnchor("Link to this section");
    $('#content').find('.wikianchor').each(function() {
        $(this).addAnchor("Link to " + $(this).attr('id'));
    });
    $('#supporters img').hover(function (event) {
        $(this).prop('src', $(this).prop('src').replace('-gray', '-color'));
    }, function (event) {
        $(this).prop('src', $(this).prop('src').replace('-color', '-gray'));
    }).each(function (i, el) {
        // Preloading
        var img = new Image();
        img.onload = function () {
            img.onload = function () {};
            img = null;
        };
        img.src = $(this).prop('src').replace('-gray', '-color');
    });
});
