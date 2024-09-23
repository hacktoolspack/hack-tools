/// jquery.dataset v0.1.0 -- HTML5 dataset jQuery plugin
/// http://orangesoda.net/jquery.dataset.html

/// Copyright (c) 2009, Ben Weaver.  All rights reserved.
/// This software is issued "as is" under a BSD license
/// <http://orangesoda.net/license.html>.  All warrenties disclaimed.

///  The HTML5 specification allows elements to have custom data
///  attributes that are prefixed with `data-'.  They may be
///  conveniently accessed through an element's `dataset' property.
///  This plugin provides similar functionality.
///
///  The methods in the plugin are designed to be similar to the
///  built-in `attr' and `data' methods.  All names are without the
///  `data-' prefix.
//
///  These methods are defined:
///
///    dataset()
///      Return an object with all custom attribute (name, value) items.
///
///    dataset(name)
///      Return the value of the attribute `data-NAME'.
///
///    dataset(name, value)
///      Set the value of attribtue `data-NAME' to VALUE.
///
///    dataset({...})
///      Set many custom attributes at once.
///
///    removeDataset(name)
///      Remove the attribute `data-NAME'.
///
///    removeDataset([n1, n2, ...])
///      Remove the attributes `data-N1', `data-N2', ...

(function($) {
     var PREFIX = 'data-',
	 PATTERN = /^data\-(.*)$/;

     function dataset(name, value) {
	 if (value !== undefined) {
	     // dataset(name, value): set the NAME attribute to VALUE.
	     return this.attr(PREFIX + name, value);
	 }

	 switch (typeof name) {
	 case 'string':
	     // dataset(name): get the value of the NAME attribute.
	     return this.attr(PREFIX + name);

	 case 'object':
	     // dataset(items): set the values of all (name, value) items.
	     return set_items.call(this, name);

	 case 'undefined':
	     // dataset(): return a mapping of (name, value) items for the
	     // first element.
	     return get_items.call(this);

	 default:
	     throw 'dataset: invalid argument ' + name;
	 }
     }

     function get_items() {
	 return this.foldAttr(function(index, attr, result) {
	     var match = PATTERN.exec(this.name);
	     if (match) result[match[1]] = this.value;
	 });
     }

     function set_items(items) {
	 for (var key in items) {
	     this.attr(PREFIX + key, items[key]);
	 }
	 return this;
     }

     function remove(name) {
	 if (typeof name == 'string') {
	     // Remove a single attribute;
	     return this.removeAttr(PREFIX + name);
	 }
	 return remove_names(name);
     }

     function remove_names(obj) {
	 var idx, length = obj && obj.length;

	 // For any object, remove attributes named by the keys.
	 if (length === undefined) {
	     for (idx in obj) {
		 this.removeAttr(PREFIX + idx);
	     }
	 }
	 // For an array, remove attributes named by the values.
	 else {
	     for (idx = 0; idx < length; idx++) {
		 this.removeAttr(PREFIX + obj[idx]);
	     }
	 }

	 return this;
     }

     $.fn.dataset = dataset;
     $.fn.removeDataset = remove_names;

})(jQuery);

(function($) {

     function each_attr(proc) {
	 if (this.length > 0) {
	     $.each(this[0].attributes, proc);
	 }
	 return this;
     }

     function fold_attr(proc, acc) {
	 return fold((this.length > 0) && this[0].attributes, proc, acc);
     }

     /*
      * A left-fold operator. The behavior is the same as $.each(),
      * but the callback is called with the accumulator as the third
      * argument.  The default accumulator is an empty object.
      */
     function fold(object, proc, acc) {
	 var length = object && object.length;

	 // The default accumulator is an empty object.
	 if (acc === undefined) acc = {};

	 // Returning an empty accumulator when OBJECT is "false"
	 // makes FOLD more composable.
	 if (!object) return acc;

	 // Check to see if OBJECT is an array.
	 if (length !== undefined) {
	     for (var i = 0, value = object[i];
		  (i < length) && (proc.call(value, i, value, acc) !== false);
		  value = object[++i])
	     { }
	 }
	 // Object is a map of (name, value) items.
	 else {
	     for (var name in object) {
		 if (proc.call(object[name], name, object[name], acc) === false) break;
	     }
	 }

	 return acc;
     }

     function fold_jquery(proc, acc) {
	 if (acc === undefined) acc = [];
	 return fold(this, proc, acc);
     }

     $.fn.eachAttr = each_attr;
     $.fn.foldAttr = fold_attr;
     $.fn.fold = fold_jquery;
     $.fold = fold;

})(jQuery);

