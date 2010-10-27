$(document).ready(function () {
	$(".folding").each(function (i) {
		var ul = $(this).next();
		if ($(this).hasClass("closed")) {
			ul.addClass("closed").hide();
		}
		else {
			ul.removeClass("closed");
		}
		$(this).click(function () {
			ul.slideToggle(400).toggleClass("closed");
			$(this).toggleClass("closed");
		});
	});

	var value = Math.round(993.97 / 1120.0 * 100) + "%";
	var progress = $("<div/>").css({
		"position": "absolute",
		"width": "500px",
		"height": "20px",
		"border": "1px solid #528F63",
		"left": "50%",
		"margin-left": "-250px",
		"background": "white",
		"top": "55px",
		"padding": "1px"
	});
	var bar = $("<div/>").css({
		"width": value,
		"height": "100%",
		"background": "#528F63"
	});
	bar.appendTo(progress);
	var text = $("<div/>").css({
		"position": "relative",
		"width": "100%",
		"top": "-20px",
		"text-align": "center"
	});
	var link = $("<a/>").attr("href", "/blog/2010/08/02/PoletnaAkcijaZbiranjaPrispevkov2010").text("Zbiramo prispevke za naslednje obdobje delovanja").css({
		"font-weight": "bold",
		"color": "#656565"
	});
	text.append(link);
	text.appendTo(progress);
	var percent = $("<div/>").css({
		"position": "relative",
		"left": "505px",
		"width": "100%",
		"top": "-36px",
		"font-weight": "bold",
		"color": "#528F63"
	}).text(value);
	percent.appendTo(progress);
	progress.appendTo($('#banner'));
});
