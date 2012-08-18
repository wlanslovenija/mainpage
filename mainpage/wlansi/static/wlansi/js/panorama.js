$.fn.panorama=function(o){

	function getCookies() {
		if (!document.cookie) return {};
		var cookies = document.cookie.split(";"), x, y, i;
		var object = {};
		for (i = 0; i < cookies.length; i++) {
			x = cookies[i].substr(0,cookies[i].indexOf("="));
			y = cookies[i].substr(cookies[i].indexOf("=")+1);
			x = x.replace(/^\s+|\s+$/g,"");
			object[x] = unescape(y);
		}
		return object;
	}

	function setCookies(object) {
		var cookies = [];
		for (var x in object) {
			if (object[x])
				cookies.push(x + "=" + escape(object[x]));
		}
		document.cookie = cookies.join("; ");
		console.log(cookies.join(";"));
		console.log(document.cookie);
	}

	var cookies = getCookies();

	var s = $.extend({images : [], transitionTime : 2000, panoramaTime : 60000}, o);

	var c = this;
	var cWidth = this.width();
	var cHeight = this.height();
	var cImage;

	var cFlow = cookies["panorama_stop"] ? false : true;

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
				style : "position : absolute; top: 0; opacity: 0; z-index: 0;" 
			});
			nImage.css("left", x1 + "px");
			nImage.css("text-indent", x1 + "px");

			c.append(nImage);
			nImage.animate({opacity: 1}, { queue: false, duration: s.transitionTime} );

			nImage.animate({"text-indent" : x2 + "px"}, { queue: false, 
				duration: s.panoramaTime, 
				easing : 'linear', step : function (now, prop) { 

					if (cFlow)
						$(prop.elem).css("left", now);
					
						//prop.start = prop.end = prop.now;
				}});

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

	var toggle = $('<a href="#">Pause</a>').addClass("toggle").attr("style", "z-index: 100; position: absolute; bottom: 10px; right: 10px; ");

	if (!cFlow) toggle.addClass("play");

	toggle.click(function (e) { 
		cFlow = !cFlow;
		$(this).html(cFlow ? "Pause" : "Play");
		$(this).toggleClass("play");
		e.preventDefault();
		document.cookie = "panorama_stop=" + (cFlow ? "" : "1") + ";";
	});

	c.append(toggle);

};
