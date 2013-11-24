(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.pup.PatientInfoView = (function(_super) {
      __extends(PatientInfoView, _super);

      function PatientInfoView() {
        this._updateModel = __bind(this._updateModel, this);
        this._renderAngle = __bind(this._renderAngle, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = PatientInfoView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatientInfoView.prototype.events = {
        'click .save-changes': '_updateModel'
      };

      PatientInfoView.prototype.initialize = function(options) {
        this.listenTo(this.model, 'change:name change:sleep_interval_ms change:sit_interval_ms', this.render);
        return this.listenTo(this.model, 'change:angle', this._renderAngle);
      };

      PatientInfoView.prototype.render = function() {
        var sitMin, sleepMin, source, template;
        this.$el.empty();
        sleepMin = this.model.get('sleep_interval_ms') / (60 * 1000);
        sitMin = this.model.get('sit_interval_ms') / (60 * 1000);
        source = $('#patient-info-template').html();
        template = Handlebars.compile(source);
        this.$el.append(template(_.defaults({
          sleepMin: sleepMin,
          sitMin: sitMin
        }, this.model.attributes)));
        return this._renderAngle;
      };

      PatientInfoView.prototype._renderAngle = function() {};

      PatientInfoView.prototype._updateModel = function() {
        var name, sitMin, sitMs, sleepMin, sleepMs;
        name = this.$('.name-input').val();
        sleepMin = this.$('.sleep-input').val();
        sitMin = this.$('.sit-input').val();
        sleepMs = parseInt(sleepMin) * 60 * 1000;
        sitMs = parseInt(sitMin) * 60 * 1000;
        return this.model.set({
          name: name,
          sleep_interval_ms: sleepMs,
          sit_interval_ms: sitMs
        });
      };

      return PatientInfoView;

    })(Backbone.View);
  })();

}).call(this);
