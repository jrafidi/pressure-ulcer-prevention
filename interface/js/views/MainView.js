(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.pup.MainView = (function(_super) {
      __extends(MainView, _super);

      function MainView() {
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = MainView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      MainView.prototype.initialize = function() {};

      MainView.prototype.render = function() {
        this.$el.empty();
        this.listView = new com.pup.PatientListView({
          model: this.model
        });
        this.listView.render();
        return this.$el.append(this.listView.$el);
      };

      return MainView;

    })(Backbone.View);
  })();

}).call(this);
