$.fn.panorama=function(o){
	var s = $.extend({images : [], transitionTime : 2000, panoramaTime : 60000}, o);

	var c = this;
	var cWidth = this.width();
	var cHeight = this.height();
	var cImage;

	c.css("overflow", "hidden");
	c.css("position", "relative");

	function changeImage(imgurl) {

		if (cImage && cImage.attr("src") == imgurl) {
			setTimeout(loadRandom, 1000);
			return;
		}

		var img = new Image();

		img.onload = function() {
			
			if (img.height < cHeight || img.width * (cHeight / img.height) < cWidth) {
				setTimeout(loadRandom, 1000);
				return;
			}

			var x = -(img.width * (cHeight / img.height) - cWidth);

			if (Math.random() > 0.5) {
				var x1 = x;
				var x2 = 0;
			} else {
				var x1 = 0;
				var x2 = x;
			}

			/*x1 = Math.round(Math.min(0, Math.max(x, x * Math.random())));
			x2 = Math.round(Math.min(0, Math.max(x, x * Math.random())));*/

			var nImage = $("<img />").attr({
				src : imgurl, 
				height : cHeight, 
				style : "position : absolute; top: 0; opacity: 0;" 
			});
			nImage.css("left", x1 + "px");

			c.append(nImage);
			nImage.animate({opacity: 1}, { queue: false, duration: s.transitionTime} );

			nImage.animate({left: x2 + "px"}, { queue: false, duration: s.panoramaTime, easing : 'linear'});

			if (cImage) {
				cImage.animate({opacity: 0}, s.transitionTime, function() {
					cImage.remove();
					cImage = nImage;
				});
			} else cImage = nImage;

			setTimeout(loadRandom, s.panoramaTime - s.transitionTime);
		}

		img.onerror = function () {

			setTimeout(loadRandom, 1000);

		}

		img.src = imgurl;

	}
	
	function loadRandom() {

		var i = Math.floor(Math.random() * o.images.length);

		var imgurl = o.images[Math.min(o.images.length-1, Math.max(i, 0))];

		changeImage(imgurl);
	}

	loadRandom();
};
