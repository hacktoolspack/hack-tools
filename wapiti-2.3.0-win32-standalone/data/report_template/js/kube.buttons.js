/*
 	kube.buttons.js v1.0.1
 	Copyright 2013 Imperavi, Inc.
*/

!function ($) {

	"use strict";

	// Plugin
	$.fn.buttons = function(option)
	{
		return this.each(function()
		{
			var $obj = $(this);

			var data = $obj.data('buttons');
			if (!data)
			{
				$obj.data('buttons', (data = new Buttons(this, option)));
			}
		});
	};

	// Initialization
	var Buttons = function(element, options)
	{
		// Element
		this.$el = $(element);

		// Options
		this.opts = $.extend({

			target: false,
			type: false

		}, options, this.$el.data());

		// Init
		this.init();
	};

	// Functionality
	Buttons.prototype = {

		// Initialization
		init: function()
		{
			if (this.opts.type === 'toggle') this.buttons = this.$el;
			else this.buttons = this.$el.find('.btn');

			if (this.opts.type === 'segmented') this.value = $(this.opts.target).val().split(',');
			else this.value = $(this.opts.target).val();

			this.buttons.each($.proxy(function(i,s)
			{
				var $s = $(s);
				if (this.opts.type === 'segmented' && $.inArray($s.val(), this.value) !== -1)
				{
					this.active($s);
				}
				else
				{
					if (this.opts.type === 'toggle' && this.value === 1) this.active($s);
					else if (this.value === $s.val()) this.active($s);
				}

				$s.click($.proxy(function(e)
				{
					e.preventDefault();

					if (this.opts.type === 'segmented')
					{
						this.value = $(this.opts.target).val().split(',');

						if (!$s.hasClass('btn-active'))
						{
							this.active($s);
							this.value.push($(s).val());
						}
						else
						{
							this.inactive($s);
							this.value.splice(this.value.indexOf($s.val()), 1);
						}

						$(this.opts.target).val(this.value.join(',').replace(/^,/, ''));

					}
					else if (this.opts.type === 'toggle')
					{
						if ($s.hasClass('btn-active'))
						{
							this.inactive($s);
							$(this.opts.target).val(0);
						}
						else
						{
							this.active($s);
							$(this.opts.target).val(1);
						}
					}
					else
					{
						this.inactive(this.buttons);
						this.active($s);
						$(this.opts.target).val($s.val());
					}
				}, this));

			}, this));
		},
		active: function($el)
		{
			$el.addClass('btn-active');
		},
		inactive: function($el)
		{
			$el.removeClass('btn-active');
		},
	};

	$(function()
	{
		$('[data-toggle="buttons"]').buttons();
	});

}(window.jQuery);