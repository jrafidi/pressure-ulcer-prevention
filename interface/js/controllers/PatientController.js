(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    return com.pup.PatientController = (function() {
      function PatientController(options) {
        this._sendMessage = __bind(this._sendMessage, this);
        this._updateSettings = __bind(this._updateSettings, this);
        this._parseMessage = __bind(this._parseMessage, this);
        this._initializeSocket = __bind(this._initializeSocket, this);
        $.extend(this, Backbone.Events);
        this.model = options.model;
        this.selectionModel = options.selectionModel;
        this._initializeSocket();
        this.listenTo(this.model, 'change', this._updateSettings);
      }

      PatientController.prototype._initializeSocket = function() {
        this.socket = new WebSocket("ws://" + com.pup.WEBSOCKET_URL + ":" + com.pup.WEBSOCKET_PORT + "/");
        return this.socket.onmessage = this._parseMessage;
      };

      PatientController.prototype._parseMessage = function(message) {
        var data, device, deviceId, ids, info, m, turns, _i, _len, _ref, _results;
        data = JSON.parse(message.data);
        if (data.type === 'state') {
          delete data['type'];
          ids = [];
          for (deviceId in data) {
            info = data[deviceId];
            ids.push(deviceId);
            if (this.model.where({
              'deviceId': parseInt(deviceId)
            }).length === 0) {
              this.model.add(new com.pup.PatientModel(info.attributes));
            }
          }
          _ref = this.model.models;
          _results = [];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            m = _ref[_i];
            if (!_.contains(ids, m.get('deviceId').toString())) {
              this.model.remove(m);
              if (this.selectionModel.get('selected') === m.cid) {
                _results.push(this.selectionModel.set('selected', null));
              } else {
                _results.push(void 0);
              }
            } else {
              _results.push(void 0);
            }
          }
          return _results;
        } else if (data.type === 'update') {
          device = this.model.where({
            'deviceId': data.deviceId
          })[0];
          device.set('angle', data.angle);
          return device.set('sleeping', data.sleeping);
        } else if (data.type === 'turn') {
          device = this.model.where({
            'deviceId': data.deviceId
          })[0];
          turns = device.get('turns').slice(0);
          turns.push(data.turn);
          return device.set('turns', turns);
        }
      };

      PatientController.prototype._updateSettings = function(patient) {
        return this._sendMessage(patient.attributes);
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
