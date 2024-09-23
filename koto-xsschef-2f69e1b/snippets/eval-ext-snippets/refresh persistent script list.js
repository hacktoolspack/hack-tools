var clone = [];
Object.keys(persistentScripts).forEach(function(key) {
    clone.push({ name: key, 
                 urlmatch: persistentScripts[key].urlmatch, 
                 code: persistentScripts[key].code.substr(0,100) + "..."
              });
});
log({type: 'report_persistent', 'result': clone});