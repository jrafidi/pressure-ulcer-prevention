(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    return com.pup.PatientController = (function() {
      function PatientController(options) {
        this._sendMessage = __bind(this._sendMessage, this);
        this._parseMessage = __bind(this._parseMessage, this);
        this._initializeSocket = __bind(this._initializeSocket, this);
        $.extend(this, Backbone.Events);
        this.model = options.model;
        this._initializeSocket();
      }

      PatientController.prototype._initializeSocket = function() {
        this.socket = new WebSocket("ws://localhost:9000/");
        return this.socket.onmessage = this._parseMessage;
      };

      PatientController.prototype._parseMessage = function(message) {};

      PatientController.prototype._sendMessage = function(data) {
        var msg;
        msg = JSON.stringify(data);
        return this.socket.send(msg);
      };

      return PatientController;

    })();
  })();

}).call(this);
