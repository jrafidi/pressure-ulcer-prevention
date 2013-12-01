(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.pup.PatientTurnView = (function(_super) {
      __extends(PatientTurnView, _super);

      function PatientTurnView() {
        this._renderTurns = __bind(this._renderTurns, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = PatientTurnView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatientTurnView.prototype.initialize = function(options) {
        return this.listenTo(this.model, 'change:turns', this.render);
      };

      PatientTurnView.prototype.render = function() {
        var source, template;
        this.$el.empty();
        source = $('#patient-turn-template').html();
        template = Handlebars.compile(source);
        this.$el.append(template({}));
        this.$('#fromDatepicker').datepicker();
        this.$('#toDatepicker').datepicker();
        return this._renderTurns();
      };

      PatientTurnView.prototype._renderTurns = function() {
        var angle, count, sortedTurns, source, t, template, turn, turns, _i, _j, _len, _len1, _ref1, _results;
        turns = [];
        sortedTurns = _.sortBy(this.model.get('turns'), function(turn) {
          return -1 * turn.startTime;
        });
        for (_i = 0, _len = sortedTurns.length; _i < _len; _i++) {
          turn = sortedTurns[_i];
          t = {};
          t.late = turn.late;
          if (turn.sleeping) {
            t.prefix = "Laying";
          } else {
            t.prefix = "Sitting";
          }
          angle = Math.round(turn.angle) * -1;
          if (angle > 0) {
            t.dir = 'right';
          } else {
            t.dir = 'left';
          }
          t.angle = Math.abs(angle);
          t.fromTime = moment(turn.startTime).format('M/D H:m');
          t.toTime = moment(turn.endTime).format('M/D H:m');
          turns.push(t);
        }
        source = $('#patient-turnlist-template').html();
        template = Handlebars.compile(source);
        this.$('.turn-list').html(template({
          turns: turns
        }));
        count = 0;
        _ref1 = this.$('.turn-item');
        _results = [];
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          turn = _ref1[_j];
          if (count % 2 === 0) {
            $(turn).addClass('dark');
          }
          _results.push(count = count + 1);
        }
        return _results;
      };

      return PatientTurnView;

    })(Backbone.View);
  })();

}).call(this);
