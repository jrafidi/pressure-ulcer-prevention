(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.pup.PatientModel = (function(_super) {
      __extends(PatientModel, _super);

      function PatientModel() {
        this.defaults = __bind(this.defaults, this);
        _ref = PatientModel.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatientModel.prototype.defaults = function() {
        return {
          deviceId: null,
          name: '',
          notes: '',
          sleep_interval_ms: 7200000,
          sit_interval_ms: 900000,
          angle: 0,
          sleeping: true,
          turns: [],
          selected: false
        };
      };

      return PatientModel;

    })(Backbone.Model);
  })();

}).call(this);
