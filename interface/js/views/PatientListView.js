(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.pup.PatientListView = (function(_super) {
      __extends(PatientListView, _super);

      function PatientListView() {
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = PatientListView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatientListView.prototype.className = 'patient-list';

      PatientListView.prototype.initialize = function() {
        return this.listenTo(this.model, 'add remove reset change:name', this.render);
      };

      PatientListView.prototype.render = function() {
        var model, source, template, _i, _len, _ref1, _results;
        this.$el.empty();
        _ref1 = this.model.models;
        _results = [];
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          model = _ref1[_i];
          source = $('#patient-item-template').html();
          template = Handlebars.compile(source);
          _results.push(this.$el.append(template(model.attributes)));
        }
        return _results;
      };

      return PatientListView;

    })(Backbone.View);
  })();

}).call(this);
