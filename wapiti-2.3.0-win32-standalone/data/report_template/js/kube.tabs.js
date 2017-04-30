/*
 	kube.tabs.js v1.0.1
 	Copyright 2013 Imperavi, Inc.
*/

!function ($) {

	"use strict";

	// Plugin
	$.fn.tabs = function(option)
	{
		return this.each(function()
		{
			var $obj = $(this);

			var data = $obj.data('tabs');
			if (!data)
			{
				$obj.data('tabs', (data = new Tabs(this, option)));
			}
		});
	};

	// Initialization
	var Tabs = function(element, options)
	{
		// Element
		this.$el = $(element);

		// Options
		this.opts = $.extend({

			height: false,
			active: false

		}, options, this.$el.data());

		// Init
		this.init();
	};

	// Functionality
	Tabs.prototype = {

		// Initialization
		init: function()
		{
			this.links = this.$el.find('a');
			this.tabs = [];

			this.links.each($.proxy(function(i,s)
			{
				var hash = $(s).attr('href');
				this.tabs.push(hash);

				if (!$(s).hasClass('active')) $(hash).hide();

				// option active
				if (this.opts.active !== false && this.opts.active === hash)
				{
					this.show(s, hash);
				}

				$(s).click($.proxy(function(e)
				{
					e.preventDefault();
					this.show(s, hash);

				}, this));

			}, this));

			// option equal
			if (this.opts.height === 'equal')
			{
				this.setMaxHeight(this.getMaxHeight());
			}
		},
		active: function(tab)
		{
			this.links.removeClass('active');
			$(tab).addClass('active');
		},
		show: function(tab, hash)
		{
			this.hide();
			$(hash).show();
			this.active(tab);
		},
		hide: function()
		{
			$.each(this.tabs, function() { $(this).hide(); });
		},
		setMaxHeight: function(height)
		{
			$.each(this.tabs, function() { $(this).css('min-height', height + 'px'); });
		},
		getMaxHeight: function()
		{
			return Math.max.apply(null, $(this.tabs).map(function() { return $(this).height(); }).get());
		}
	};

	$(function()
	{
		$('nav[data-toggle="tabs"]').tabs();
	});

}(window.jQuery);