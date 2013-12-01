do ->
  class com.pup.PatientTurnView extends Backbone.View

    initialize: (options) =>
      @listenTo @model, 'change:turns', @render

    render: =>
      @$el.empty()
      source = $('#patient-turn-template').html()
      template = Handlebars.compile(source)
      @$el.append template({})

      @$('#fromDatepicker').datepicker()
      @$('#toDatepicker').datepicker()

      @_renderTurns()

    _renderTurns: =>
      turns = []
      sortedTurns = _.sortBy(@model.get('turns'), (turn) -> return -1 * turn.startTime)
      for turn in sortedTurns
        t = {}
        t.late = turn.late

        if turn.sleeping
          t.prefix = "Laying"
        else
          t.prefix = "Sitting"

        angle = Math.round(turn.angle) * -1
        if angle > 0
          t.dir = 'right'
        else
          t.dir = 'left'
        t.angle = Math.abs(angle)

        t.fromTime = moment(turn.startTime).format('M/D H:m')
        t.toTime = moment(turn.endTime).format('M/D H:m')
        turns.push(t)

      source = $('#patient-turnlist-template').html()
      template = Handlebars.compile(source)
      @$('.turn-list').html template({turns: turns})

      count = 0
      for turn in @$('.turn-item')
        if count%2 == 0
          $(turn).addClass('dark')
        count = count + 1