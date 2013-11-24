(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.pup.PatientContentView = (function(_super) {
      __extends(PatientContentView, _super);

      function PatientContentView() {
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = PatientContentView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatientContentView.prototype.className = 'patient-content';

      PatientContentView.prototype.initialize = function(options) {
        this.selectionModel = options.selectionModel;
        return this.listenTo(this.selectionModel, 'change', this.render);
      };

      PatientContentView.prototype.render = function() {
        var cid, patient, source, template;
        this.$el.empty();
        if (this.selectionModel.get('selected') == null) {
          return this.$el.append($('<div class="nothing"/>').text('Select a patient on the left.'));
        } else {
          source = $('#patient-content-template').html();
          template = Handlebars.compile(source);
          this.$el.append(template({}));
          cid = this.selectionModel.get('selected');
          patient = this.model.get(cid);
          this.infoView = new com.pup.PatientInfoView({
            model: patient,
            el: this.$('.patient-content-top')
          });
          return this.infoView.render();
        }
      };

      return PatientContentView;

    })(Backbone.View);
  })();

}).call(this);
