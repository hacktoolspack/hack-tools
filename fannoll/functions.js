

function load() {
	var imgs = load.arguments;
	if (document.images) {
		if (document.preload == null) document.preload = new Array();
		var i = document.preload.length;
		for (var j = 0; j < imgs.length; j++) {
			document.preload[i] = new Image();
			document.preload[i++].src = imgs[j];
		}
	}
}

function restore(){ 
	var i, x, a = document.swaps; 
	if( a ) for( i = 0; i < a.length; i++)
		if( a[i].oldSrc ) a[i].src=a[i].oldSrc;
}

function swap(){ 
	var i, j = 0, a = swap.arguments; 
	document.swaps = new Array; 
	for( i = 0; i < ( a.length - 1 ); i += 2 ){
		document.swaps[j++] = a[i];
		if( !a[i].oldSrc ) a[i].oldSrc = a[i].src;
		a[i].src = a[i + 1];
	}
}

function openW(url, name, w, h) {
	var windowprops = "width=" + w + ",height=" + h;
	popup = window.open(url, name, windowprops);
	setTimeout('popup.focus();',250);
}
