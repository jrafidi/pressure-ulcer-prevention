do ->
  BUCKET_SIZE = 10
  MIN = -60
  MAX = 60
  class com.pup.PatientTurnView extends Backbone.View

    initialize: (options) =>
      @listenTo @model, 'change:turns', @_renderTurns

    render: =>
      @$el.empty()
      source = $('#patient-turn-template').html()
      template = Handlebars.compile(source)
      @$el.append template({})

      @$('#fromDatepicker').datepicker(
          onSelect: @_renderTurns
        )
      @$('#toDatepicker').datepicker(
          onSelect: @_renderTurns
        )

      @$('#fromDatepicker').datepicker('setDate', new Date())
      @$('#toDatepicker').datepicker('setDate', new Date())

      @barchart = d3.select('.turn-chart')
        .append('svg')
        .attr('height', 220)
        .attr('width', 400)
        .chart('BarChart')

      @_renderTurns()

    _renderTurns: =>
      turns = []
      sortedTurns = _.sortBy(@model.get('turns'), (turn) -> return -1 * turn.startTime)

      from = moment(@$('#fromDatepicker').datepicker('getDate'))
      to = moment(@$('#toDatepicker').datepicker('getDate'))
      to.add('days', 1)

      for turn in sortedTurns
        t = {}

        fromTime = moment(turn.startTime)
        toTime = moment(turn.endTime)
        t.startTime = turn.startTime
        t.endTime = turn.endTime

        if (fromTime.isBefore(to) and fromTime.isAfter(from)) or (toTime.isBefore(to) and toTime.isAfter(from))
          t.late = turn.late
          t.fromTime = fromTime.format('MM/DD HH:mm')
          t.toTime = toTime.format('MM/DD HH:mm')

          if turn.sleeping
            t.prefix = "Laying"
          else
            t.prefix = "Sitting"

          angle = Math.round(turn.angle) * -1
          if angle > 0
            t.dir = 'right'
          else
            t.dir = 'left'
          t.rawAngle = angle
          t.angle = Math.abs(angle)
          turns.push(t)

      if turns.length > 0
        source = $('#patient-turnlist-template').html()
        template = Handlebars.compile(source)
        @$('.turn-list').html template({turns: turns})
        count = 0
        for turn in @$('.turn-item')
          if count%2 == 0
            $(turn).addClass('dark')
          count = count + 1
      else
        @$('.turn-list').html $('<div class="no-turns"/>').text('No posture history in selected range')
      @_processTurnChart(turns)

    _processTurnChart: (turns) =>
      data = []
      for i in [MIN/BUCKET_SIZE..MAX/BUCKET_SIZE]
        data.push
          name: "#{Math.abs(i)*BUCKET_SIZE}\xB0"
          value: 0
          sum: 0
          center: i * BUCKET_SIZE

      total = 0
      for turn in turns
        turnTime = turn.endTime - turn.startTime
        total += turnTime
        for bucket in data
          max = bucket.center + BUCKET_SIZE / 2
          min = bucket.center - BUCKET_SIZE / 2
          if turn.rawAngle < max and turn.rawAngle >= min
            bucket.sum = bucket.sum + turnTime

      max = 0
      for bucket in data
        bucket.value = (bucket.sum / total)
        if bucket.value > max
          max = bucket.value

      @barchart.draw(data)
      @barchart.max(max * 1.1)