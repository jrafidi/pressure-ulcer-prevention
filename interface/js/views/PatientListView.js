(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref, _ref1;
    com.pup.PatientListView = (function(_super) {
      __extends(PatientListView, _super);

      function PatientListView() {
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = PatientListView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatientListView.prototype.className = 'patient-list';

      PatientListView.prototype.initialize = function(options) {
        this.selectionModel = options.selectionModel;
        return this.listenTo(this.model, 'add remove reset', this.render);
      };

      PatientListView.prototype.render = function() {
        var listItem, m, _i, _len, _ref1, _results;
        this.$el.empty();
        _ref1 = this.model.models;
        _results = [];
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          m = _ref1[_i];
          listItem = new com.pup.PatientListItem({
            model: m,
            selectionModel: this.selectionModel
          });
          listItem.render();
          _results.push(this.$el.append(listItem.$el));
        }
        return _results;
      };

      return PatientListView;

    })(Backbone.View);
    return com.pup.PatientListItem = (function(_super) {
      __extends(PatientListItem, _super);

      function PatientListItem() {
        this._selectModel = __bind(this._selectModel, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref1 = PatientListItem.__super__.constructor.apply(this, arguments);
        return _ref1;
      }

      PatientListItem.prototype.className = 'patient-item';

      PatientListItem.prototype.events = {
        'click': '_selectModel'
      };

      PatientListItem.prototype.initialize = function(options) {
        this.selectionModel = options.selectionModel;
        this.listenTo(this.model, 'change:name', this.render);
        return this.listenTo(this.selectionModel, 'change', this.render);
      };

      PatientListItem.prototype.render = function() {
        var source, template;
        this.$el.empty();
        source = $('#patient-item-template').html();
        template = Handlebars.compile(source);
        this.$el.append(template(this.model.attributes));
        if (this.selectionModel.get('selected') === this.model.cid) {
          return this.$el.addClass('selected');
        } else {
          return this.$el.removeClass('selected');
        }
      };

      PatientListItem.prototype._selectModel = function() {
        return this.selectionModel.set('selected', this.model.cid);
      };

      return PatientListItem;

    })(Backbone.View);
  })();

}).call(this);
