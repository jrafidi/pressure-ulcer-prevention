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

      MainView.prototype.initialize = function(options) {
        return this.selectionModel = options.selectionModel;
      };

      MainView.prototype.render = function() {
        var source, template;
        this.$el.empty();
        source = $('#top-bar-template').html();
        template = Handlebars.compile(source);
        this.$el.append(template({}));
        this.listView = new com.pup.PatientListView({
          model: this.model,
          selectionModel: this.selectionModel
        });
        this.listView.render();
        this.contentView = new com.pup.PatientContentView({
          model: this.model,
          selectionModel: this.selectionModel
        });
        this.contentView.render();
        this.$el.append(this.listView.$el);
        return this.$el.append(this.contentView.$el);
      };

      return MainView;

    })(Backbone.View);
  })();

}).call(this);
