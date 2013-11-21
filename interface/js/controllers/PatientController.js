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
        this.selectionModel = options.selectionModel;
        this._initializeSocket();
      }

      PatientController.prototype._initializeSocket = function() {
        this.socket = new WebSocket("ws://localhost:" + com.pup.WEBSOCKET_PORT + "/");
        return this.socket.onmessage = this._parseMessage;
      };

      PatientController.prototype._parseMessage = function(message) {
        var data, deviceId, ids, info, m, _i, _len, _ref;
        data = JSON.parse(message.data);
        if (data.type === 'state') {
          delete data['type'];
          ids = [];
          for (deviceId in data) {
            info = data[deviceId];
            ids.push(deviceId);
            if (this.model.where({
              'deviceId': deviceId
            }).length === 0) {
              this.model.add(new com.pup.PatientModel(info.attributes));
            }
          }
          _ref = this.model.models;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            m = _ref[_i];
            if (!_.contains(ids, m.get('deviceId').toString())) {
              this.model.remove(m);
              if (this.selectionModel.get('selected') === m.cid) {
                this.selectionModel.set('selected', null);
              }
            }
          }
          return console.log(this.model.models);
        }
      };

      PatientController.prototype._sendMessage = function(data) {
        var msg;
        msg = JSON.stringify(data);
        return this.socket.send(msg);
      };

      return PatientController;

    })();
  })();

}).call(this);
