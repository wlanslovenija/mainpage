$.fn.visage.defaults.files = {
	"blank": "/chrome/site/blank.gif",
	"error": "/chrome/site/error.png"
};
$.fn.visage.defaults.attr.image.src = "/chrome/site/blank.gif";
$.fn.visage.defaults.addDOM = function (visageDOM, options) {
	$.fn.visage.addDOM(visageDOM, options);
	// Moves elements to overlay so they are all in the same stacking context
	$(visageDOM.prev).add(visageDOM.next).add(visageDOM.count).add(visageDOM.title).appendTo(visageDOM.overlay);
};
$.fn.visage.defaults.imageValues = function (image, options) {
	var values = $.fn.visage.imageValues(image, options);
	values.src = values.src.replace(/^\/attachment\//, "/raw-attachment/");
	return values;
};
$(document).ready(function () {
	$("a[href^='/attachment/']:has(img)").visage();
});
