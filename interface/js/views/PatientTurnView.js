(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var BUCKET_SIZE, MAX, MIN, _ref;
    BUCKET_SIZE = 10;
    MIN = -60;
    MAX = 60;
    return com.pup.PatientTurnView = (function(_super) {
      __extends(PatientTurnView, _super);

      function PatientTurnView() {
        this._processTurnChart = __bind(this._processTurnChart, this);
        this._renderTurns = __bind(this._renderTurns, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = PatientTurnView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatientTurnView.prototype.initialize = function(options) {
        return this.listenTo(this.model, 'change:turns', this._renderTurns);
      };

      PatientTurnView.prototype.render = function() {
        var source, template;
        this.$el.empty();
        source = $('#patient-turn-template').html();
        template = Handlebars.compile(source);
        this.$el.append(template({}));
        this.$('#fromDatepicker').datepicker({
          onSelect: this._renderTurns
        });
        this.$('#toDatepicker').datepicker({
          onSelect: this._renderTurns
        });
        this.$('#fromDatepicker').datepicker('setDate', new Date());
        this.$('#toDatepicker').datepicker('setDate', new Date());
        this.barchart = d3.select('.turn-chart').append('svg').attr('height', 220).attr('width', 400).chart('BarChart');
        return this._renderTurns();
      };

      PatientTurnView.prototype._renderTurns = function() {
        var angle, count, from, fromTime, sortedTurns, source, t, template, to, toTime, turn, turns, _i, _j, _len, _len1, _ref1;
        turns = [];
        sortedTurns = _.sortBy(this.model.get('turns'), function(turn) {
          return -1 * turn.startTime;
        });
        from = moment(this.$('#fromDatepicker').datepicker('getDate'));
        to = moment(this.$('#toDatepicker').datepicker('getDate'));
        to.add('days', 1);
        for (_i = 0, _len = sortedTurns.length; _i < _len; _i++) {
          turn = sortedTurns[_i];
          t = {};
          fromTime = moment(turn.startTime);
          toTime = moment(turn.endTime);
          t.startTime = turn.startTime;
          t.endTime = turn.endTime;
          if ((fromTime.isBefore(to) && fromTime.isAfter(from)) || (toTime.isBefore(to) && toTime.isAfter(from))) {
            t.late = turn.late;
            t.fromTime = fromTime.format('MM/DD HH:mm');
            t.toTime = toTime.format('MM/DD HH:mm');
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
            t.rawAngle = angle;
            t.angle = Math.abs(angle);
            turns.push(t);
          }
        }
        if (turns.length > 0) {
          source = $('#patient-turnlist-template').html();
          template = Handlebars.compile(source);
          this.$('.turn-list').html(template({
            turns: turns
          }));
          count = 0;
          _ref1 = this.$('.turn-item');
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            turn = _ref1[_j];
            if (count % 2 === 0) {
              $(turn).addClass('dark');
            }
            count = count + 1;
          }
        } else {
          this.$('.turn-list').html($('<div class="no-turns"/>').text('No posture history in selected range'));
        }
        return this._processTurnChart(turns);
      };

      PatientTurnView.prototype._processTurnChart = function(turns) {
        var bucket, data, i, max, min, total, turn, turnTime, _i, _j, _k, _l, _len, _len1, _len2, _ref1, _ref2;
        data = [];
        for (i = _i = _ref1 = MIN / BUCKET_SIZE, _ref2 = MAX / BUCKET_SIZE; _ref1 <= _ref2 ? _i <= _ref2 : _i >= _ref2; i = _ref1 <= _ref2 ? ++_i : --_i) {
          data.push({
            name: "" + (Math.abs(i) * BUCKET_SIZE) + "\xB0",
            value: 0,
            sum: 0,
            center: i * BUCKET_SIZE
          });
        }
        total = 0;
        for (_j = 0, _len = turns.length; _j < _len; _j++) {
          turn = turns[_j];
          turnTime = turn.endTime - turn.startTime;
          total += turnTime;
          for (_k = 0, _len1 = data.length; _k < _len1; _k++) {
            bucket = data[_k];
            max = bucket.center + BUCKET_SIZE / 2;
            min = bucket.center - BUCKET_SIZE / 2;
            if (turn.rawAngle < max && turn.rawAngle >= min) {
              bucket.sum = bucket.sum + turnTime;
            }
          }
        }
        max = 0;
        for (_l = 0, _len2 = data.length; _l < _len2; _l++) {
          bucket = data[_l];
          bucket.value = bucket.sum / total;
          if (bucket.value > max) {
            max = bucket.value;
          }
        }
        this.barchart.draw(data);
        return this.barchart.max(max * 1.1);
      };

      return PatientTurnView;

    })(Backbone.View);
  })();

}).call(this);
