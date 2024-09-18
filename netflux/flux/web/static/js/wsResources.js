/*
 * My Websocket resources V 4.0
 */
var WebsocketClass = function WebSockets(options) {
	var self = this;
	var defaults = {
	  protocol: window.location.protocol,
	  host: window.location.host,
	  pathname: window.location.pathname,
      onMessageCallback: _callback,
      onOpenCallback: _callback,
      onCloseCallback: _callback,
	};
	var opt = $.extend(defaults, options);
	var socket = null;

	this.ws_path = (window.location.protocol=="https:") ? "wss://" : "ws://";
	this.ws_path += opt.host + opt.pathname;

 	this.host = window.location.protocol + "//" + window.location.host + opt.pathname;
    if (!window.WebSocket) { if (window.MozWebSocket) { window.WebSocket = window.MozWebSocket;} else {showMessage("Your browser doesn't support WebSockets") }}

	// private methods
	function _callback(arg) {}

	function _toJsonMessage(type, payload) {
		var message = (typeof payload == 'undefined') ? {} : payload;
		//console.log(type); console.log(message);
		return JSON.stringify({'type': type, 'text': message});
	}

	function _toMqttMessage(type, topic, payload) {
		var msg = (typeof payload == 'undefined') ? {} : payload;
		var top = (typeof topic == 'undefined')   ? '' : topic;
		return _toJsonMessage(type, {topic: top, payload: msg});
	}

  	function _connect() {
    	socket = new ReconnectingWebSocket(self.ws_path);
        socket.onmessage = function (resp) 	{ return opt.onMessageCallback(resp); };
        socket.onopen = function(event) 	{ console.log("Connected to socket: "+ self.ws_path); return opt.onOpenCallback(event); };
        socket.onclose = function(event) 	{ console.error('WebSockets closed unexpectedly'); return opt.onCloseCallback(event); };
  	}

	function _disconnect() 					{ socket.close();}
	function _send(type, payload) 			{ socket.send(_toJsonMessage(type, payload));}
	function _mqtt(type, topic, payload) 	{ socket.send(_toMqttMessage(type, topic, payload)); }

  	this.connect 	= function() { _connect();   };
    this.deconnect 	= function() { _disconnect(); };
    this.send 		= function(type, msg)	{ _send(type, msg); };
    this.mqtt 		= function(type, topic, payload) { _mqtt(type, topic, payload); };
}

let wsObject = null;

