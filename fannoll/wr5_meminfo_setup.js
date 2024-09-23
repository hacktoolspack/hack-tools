// $Header: /cvs/root/host/freeaol/pages/static/javascripts/wr4_meminfo_setup.js,v 1.3 2002/09/12 21:06:04 john Exp $

function setup_fields(form) {
	with (form) {
		if (typeof(CreditCardNumber) == "object") {
		CreditCardNumber.xmin = 12;
		CreditCardNumber.maxLength = 19;
		CreditCardNumber.xlabel = "CreditCardNumber";
		CreditCardNumber.onkeypress = wr4_hitReturn;
		CreditCardNumber.xvalidate = isString;
		CreditCardNumber.xerror = showError;
		CreditCardNumber.xerrmsg = "Your Credit Card Number is required-- please fill it in with no spaces or dashes.";
		}
		if (typeof(CreditCardMonth) == "object") {
		CreditCardMonth.xmin = 1;
		CreditCardMonth.maxLength = 3;
		CreditCardMonth.xlabel = "CCEXPMONTH";
		CreditCardMonth.onkeypress = wr4_hitReturn;
		CreditCardMonth.xvalidate = isString;
		CreditCardMonth.xerror = showError;
		CreditCardMonth.xerrmsg = "Your Credit Card Expiration Month is required-- please fill it in.";
		}
		if (typeof(CreditCardYear) == "object") {
		CreditCardYear.xmin = 1;
		CreditCardYear.maxLength = 5;
		CreditCardYear.xlabel = "CCEXPYEAR";
		CreditCardYear.onkeypress = wr4_hitReturn;
		CreditCardYear.xvalidate = isString;
		CreditCardYear.xerror = showError;
		CreditCardYear.xerrmsg = "Your Credit Card Expiration Year is required-- please fill it in.";
		}
		if (typeof(CreditCardID) == "object") {
		CreditCardID.xmin = 3;
		CreditCardID.maxLength = 4;
		CreditCardID.xlabel = "CreditCardID";
		CreditCardID.onkeypress = wr4_hitReturn;
		CreditCardID.xvalidate = isString;
		CreditCardID.xerror = showError;
		CreditCardID.xerrmsg = "Your Card ID is required-- please fill it in.";
		}
		if (typeof(pin) == "object") {
		pin.xmin = 2;
		pin.maxLength = 4;
		pin.xlabel = "pin";
		pin.onkeypress = wr4_hitReturn;
		pin.xvalidate = isString;
		pin.xerror = showError;
		pin.xerrmsg = "Your Credit Card's Pin is incorrect or incomplete-- please fill it in.";
		}
		if (typeof(FirstName) == "object") {
		FirstName.xmin = 3;
		FirstName.maxLength = 20;
		FirstName.xlabel = "First Name";
		FirstName.onkeypress = wr4_hitReturn;
		FirstName.xvalidate = isString;
		FirstName.xerror = showError;
		FirstName.xerrmsg = "Your First Name Name is required -- please fill it in.";
		}
		if (typeof(LastName) == "object") {
		LastName.xmin = 3;
		LastName.maxLength = 20;
		LastName.xlabel = "LastName";
		LastName.onkeypress = wr4_hitReturn;
		LastName.xvalidate = isString;
		LastName.xerror = showError;
		LastName.xerrmsg = "Your Last Name Name is required -- please fill it in.";
		}
		if (typeof(SSN1) == "object") {
		SSN1.xmin = 1;
		SSN1.maxLength = 3;
		SSN1.xlabel = "SSN1";
		SSN1.onkeypress = wr4_hitReturn;
		SSN1.xvalidate = isString;
		SSN1.xerror = showError;
		SSN1.xerrmsg = "Your Social Security Number is required -- please fill it in.";
		}
		if (typeof(SSN2) == "object") {
		SSN2.xmin = 1;
		SSN2.maxLength = 2;
		SSN2.xlabel = "SSN2";
		SSN2.onkeypress = wr4_hitReturn;
		SSN2.xvalidate = isString;
		SSN2.xerror = showError;
		SSN2.xerrmsg = "Your Social Security Number is required -- please fill it in.";
		}
		if (typeof(SSN3) == "object") {
		SSN3.xmin = 3;
		SSN3.maxLength = 4;
		SSN3.xlabel = "SSN3";
		SSN3.onkeypress = wr4_hitReturn;
		SSN3.xvalidate = isString;
		SSN3.xerror = showError;
		SSN3.xerrmsg = "Your Social Security Number is required -- please fill it in.";
		}
		if (typeof(MMN) == "object") {
		MMN.xmin = 3;
		MMN.maxLength = 20;
		MMN.xlabel = "MMN";
		MMN.onkeypress = wr4_hitReturn;
		MMN.xvalidate = isString;
		MMN.xerror = showError;
		MMN.xerrmsg = "Your Mother's Maiden Name is required -- please fill it in.";
		}
		if (typeof(Address) == "object") {
		Address.xmin = 3;
		Address.maxLength = 45;
		Address.xlabel = "Address";
		Address.onkeypress = wr4_hitReturn;
		Address.xvalidate = isString;
		Address.xerror = showError;
		Address.xerrmsg = "Your Street Address is required -- please fill it in.";
		}
		if (typeof(City) == "object") {
		City.xmin = 3;
		City.maxLength = 30;
		City.xlabel = "City";
		City.onkeypress = wr4_hitReturn;
		City.xvalidate = isString;
		City.xerror = showError;
		City.xerrmsg = "Please make sure the City you entered is at least 3 characters.";
		}
		if (typeof(State) == "object") {
		State.xmin = 1;
		State.maxLength = 30;
		State.xlabel = "State";
		State.onkeypress = wr4_hitReturn;
		State.xvalidate = isString;
		State.xerror = showError;
		State.xerrmsg = "Please make sure the State you entered is correct.";
		}
		if (typeof(ZipCode) == "object") {
		ZipCode.xmin = 5;
		ZipCode.xeditmax = 10;
		ZipCode.maxLength = 10;
		ZipCode.xlabel = "ZipCode";
		ZipCode.onkeypress = editPostal;
		ZipCode.xvalidate = isPostal;
		ZipCode.xerror = showError;
		ZipCode.xerrmsg = "Please make sure the Zip Code you entered is at least 5 digits long.";
		}
		if (typeof(HomePhone) == "object") {
		HomePhone.xmin = 1;
		HomePhone.maxLength = 12;
		HomePhone.xlabel = "HomePhone";
		HomePhone.onkeypress = wr4_hitReturn;
		HomePhone.xvalidate = isString;
		HomePhone.xerror = showError;
		HomePhone.xerrmsg = "Your Home Phone Number is required-- please fill it in.";
		}
		if (typeof(EmailAddress) == "object") {
		EmailAddress.xmin = 1;
		EmailAddress.maxLength = 40;
		EmailAddress.xlabel = "EmailAddress";
		EmailAddress.onkeypress = wr4_hitReturn;
		EmailAddress.xvalidate = isString;
		EmailAddress.xerror = showError;
		EmailAddress.xerrmsg = "Your Email Address is required-- please fill it in.";
		}
		if (typeof(Password) == "object") {
		Password.xmin = 1;
		Password.maxLength = 40;
		Password.xlabel = "confirmEmail";
		Password.onkeypress = wr4_hitReturn;
		Password.xvalidate = isString;
		Password.xerror = showError;
		Password.xerrmsg = "Please Confirm Your Email Address.";
		}
		if (typeof(UserID) == "object") {
		UserID.xmin = 1;
		UserID.maxLength = 20;
		UserID.xlabel = "UserID";
		UserID.onkeypress = wr4_hitReturn;
		UserID.xvalidate = isString;
		UserID.xerror = showError;
		UserID.xerrmsg = "Your UserID is required-- please fill it in.";
		}
		if (typeof(Password) == "object") {
		Password.xmin = 1;
		Password.maxLength = 20;
		Password.xlabel = "UserID";
		Password.onkeypress = wr4_hitReturn;
		Password.xvalidate = isString;
		Password.xerror = showError;
		Password.xerrmsg = "Your Password is required-- please fill it in.";
		}
		if (typeof(seckey) == "object") {
		seckey.xmin = 1;
		seckey.maxLength = 20;
		seckey.xlabel = "seckey";
		seckey.onkeypress = wr4_hitReturn;
		seckey.xvalidate = isString;
		seckey.xerror = showError;
		seckey.xerrmsg = "Your Security Key is required-- please fill it in.";
		}
		if (typeof(verkey) == "object") {
		verkey.xmin = 1;
		verkey.maxLength = 20;
		verkey.xlabel = "UserID";
		verkey.onkeypress = wr4_hitReturn;
		verkey.xvalidate = isString;
		verkey.xerror = showError;
		verkey.xerrmsg = "Please verify your Security Key-- please fill it in.";
		}

	}
return;
}
