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
    $('.hoveanimation').each(function (i, el) {
        var static_image = $(el).attr('src');
        var animation = $(el).data('animation');
        if (animation) {
            $(el).hover(function (event) {
                $(el).attr('src', animation)
            }, function (event) {
                $(el).attr('src', static_image)
            });
            var preload = new Image();
            preload.onload = function () {
                preload.onload = function () {};
                preload = null;
            };
            preload.src = animation;
        }
    });
    $('.paypal-buynow-form').submit(function (event) {
        event.preventDefault();
        $.post($(this).attr('action'), $(this).serialize(), function (data, textStatus, jqXHR) {
            $(data).addClass('hidden').appendTo('body').submit();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            console.error(jqXHR.responseText, jqXHR.status, textStatus, errorThrown);
            if (jqXHR.responseText) {
                alert(jqXHR.responseText);
            }
        });
    })
});
