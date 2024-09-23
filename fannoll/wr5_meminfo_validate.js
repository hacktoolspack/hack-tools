// $Header: /cvs/root/host/freeaol/pages/static/javascripts/wr4_meminfo_validate.js,v 1.4 2002/09/24 13:11:38 john Exp $

// Validation functions.

function showError(msgpat) {
	if (typeof(this.xerrmsg1) == "string") {
	this.xerrmsg = this.xerrmsg1 + this.value + this.xerrmsg2;
	}
alert(this.xerrmsg);
this.focus();
return false;
}

function isString() {
if (!this.value && this.xmin > 0) return(this.xerror());
	if (this.xmin > 0) {
	str = trimString(this.value);
		if (str.length < this.xmin) return(this.xerror());
	}
	if (this.value.length < this.xmin) return(this.xerror());
	if (this.value.length > this.maxLength) return(this.xerror());
return true;
}

function isNumStr() {
var str;
	if (!this.value && this.xmin > 0) return(this.xerror());
	if (this.value.match(/\D/)) return(this.xerror());
	if (this.value.length < this.xmin) return(this.xerror());
	if (this.value.length > this.maxlength) return(this.xerror());
return true;
}

function isPostal() {
code = this.value.replace(/\D/g, "");
	if (!code) return(this.xerror());
	if (code.length < this.xmin) return(this.xerror());
	if (code.length > this.xeditmax) return(this.xerror());
return true;
}

function isPhone() {
var phone;
var prefix;
var exchange;
var bad_no;
var msg;

	if (!this.value) return(this.xerror());

phone = this.value.replace(/\D/g, "");
prefix = phone.slice(0,3);
exchange = phone.slice(3,6);
bad_no = phone.slice(3,4);
msg = "The Phone Number you entered is invalid.  Please enter your evening Phone Number.";

	if (prefix == 000) return(alert(msg));this.focus();
	if (prefix == 555) return(alert(msg));this.focus();
	if (prefix == 700) return(alert(msg));this.focus();
	if (prefix == 800) return(alert(msg));this.focus();
	if (prefix == 888) return(alert(msg));this.focus();
	if (prefix == 900) return(alert(msg));this.focus();
	if (exchange == 555) return(alert(msg));this.focus();
	if (exchange == 000) return(alert(msg));this.focus();
	if (exchange == 976) return(alert(msg));this.focus();
	if (bad_no == 0) return(alert(msg));this.focus();
	if (phone.length < this.xmin) return(this.xerror());
	if (phone.length > this.xeditmax) return(this.xerror());

this.value = phone.replace(/^(\d\d\d)(\d\d\d)(\d\d\d\d)$/, "($1) $2-$3");
return true;
}

function editPostal(evt) {
IE = document.all;

	if (IE) {
	var keycode = window.event.keyCode;
	var shift   = window.event.shiftKey;
	var ctrl    = window.event.ctrlKey;
	var alt     = window.event.altKey;
	var pos     = this.value.length + 1;
	var upper   = (shift && !ctrl && !alt && keycode >= 65 && keycode <= 90);
	var lower   = (!shift && !ctrl && !alt && keycode >= 97 && keycode <= 122);
	var space   = (!shift && !ctrl && !alt && keycode == 32);
	var digit   = (!shift && !ctrl && !alt && keycode >= 48 && keycode <= 57);
		if (pos <= 5 && digit) return true;
		if (keycode == 13) wr4_hitReturn(); return false;
	} else {
	keycode = evt.which;
	var bs = String.fromCharCode(evt.which);
		if (keycode == 13) wr4_hitReturn();
		if (keycode >= 48 && keycode <= 57) return true;
		if (keycode == 0) return true;
		if (bs == "\b") return true;
	}
return false;
}

function editPhone(evt) {
IE = document.all;

        if (IE) {
        var keycode = window.event.keyCode;
        var shift   = window.event.shiftKey;
        var ctrl    = window.event.ctrlKey;
        var alt     = window.event.altKey;
	var pos = this.value.length + 1;
        //var pos = Math.ceil(document.selection.createRange().offsetLeft/7);
        ctr = document.selection.createRange();
 
        var lparen  = (shift  && !ctrl && !alt && keycode == 40);
        var rparen  = (shift  && !ctrl && !alt && keycode == 41);
        var space   = (!shift && !ctrl && !alt && keycode == 32);
        var dash    = (!shift && !ctrl && !alt && keycode == 45);
        var slash   = (!shift && !ctrl && !alt && keycode == 47);
        var digit   = (!shift && !ctrl && !alt && keycode >= 48 && keycode <= 57);

	if (keycode == 13) wr4_hitReturn();
	//if(document.selection.createRange().text.length<1 || document.selection.createRange().text.length==14) {

                if (!lparen && !rparen && !space && !dash && !digit) return false;
                if (pos == 1  && lparen) return true;
                if (pos == 1  && digit) { this.value = '('; return true; }
                if (pos == 2  && digit) return true;
                if (pos == 3  && digit) return true;
                if (pos == 4  && digit) return true;
                if (pos == 5  && rparen) { this.value += ') '; return false; }
                if (pos == 5  && dash)   { this.value += ') '; return false; }
                if (pos == 5  && slash)  { this.value += ') '; return false; }
                if (pos == 5  && space)  { this.value += ') '; return false; }
                if (pos == 5  && digit)  { this.value += ') '; return true; }
                if (pos == 6  && space) return true;
                if (pos == 6  && digit) { this.value += ' '; return true; }
                if (pos == 7  && digit) return true;
                if (pos == 8  && digit) return true;
                if (pos == 9  && digit) return true;
                if (pos == 10 && dash) return true;
                if (pos == 10 && space) { this.value += '-'; return false; }
                if (pos == 10 && digit) { this.value += '-'; return true; }
                if (pos == 11 && digit) return true;
                if (pos == 12 && digit) return true;
                if (pos == 13 && digit) return true;
                if (pos == 14 && digit) return true;
        } else {
        keycode = evt.which;
        var bs = String.fromCharCode(evt.which);
                if (keycode >= 48 && keycode <= 57) return true;
                if (keycode == 0) return true;
                if ((keycode == 32) || (keycode >= 40 && keycode <= 41) || (keycode >= 45 && keycode <= 46)) return true;
                if (bs == "\b") return true;
		if (keycode == 13) wr4_hitReturn(); return false;
        }
return false;
}

function isEmail() {
	if (this.value == "") return true;

var pattern =/.+@.+\..+/;

	if (this.value.match(pattern)) {
	return true;
	} else {
	return this.xerror();
	}
}

function trimString (str) {
str = this != window? this : str;
return str.replace(/^\s+/g, '').replace(/\s+$/g, '');
}

function wr4_isEmail(email) {
	if(email.indexOf('@') > -1 && email.indexOf('.') > -1) return true
	alert('Please specify a valid email address.'); return false ;
}

function wr4_isNull (str,tchar) {
	if (str.length == 0) {
	alert(friendlyName + ' can not be left blank.');return false;
	}
	while (str.indexOf(tchar) == 0 && str.length > 0) {
	str = str.substring(tchar.length);
	}
	while (str.lastIndexOf(tchar) == (str.length - (tchar.length)) && str.length > 0) {
	str = str.substring(0,(str.length - (tchar.length)));
	}
	if(str=="") {
	alert(friendlyName + ' can not be left blank.'); return false;
	}
return true;
}
