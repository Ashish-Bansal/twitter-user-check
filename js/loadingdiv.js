(function($) {
	var loading_bar_html = '<div class="loading-bar"></div>';
	$.fn.loadingdiv = function(options) {
		var settings = $.extend({
			number : 8,
			color : '#000',
			callback : null,
			animation_time : 0.27,
			width: '10px',
			height: '10px'
		}, options);

		return this.each(function() {
			var domHtml = '';
			for (var i = 0; i < settings.number; i++) {
				domHtml += loading_bar_html;
			}
			$(this).append(domHtml);
			var loading_bar_list = $(".loading-bar");
			console.log(loading_bar_list.length);
			for(var x=1; x <= loading_bar_list.length; x++){
				delay = (settings.animation_time/settings.number)*(x-1)+"s";
				loading_bar_list.eq(x-1).css({
					"animation-delay" : delay,
					"background-color" : settings.color,
					width: settings.width,
					height: settings.height
				});
			}

			if ($.isFunction(settings.callback)) {
				settings.callback.call(this);
			}
		});
	};
}(jQuery));
