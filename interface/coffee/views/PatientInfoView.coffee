do ->
  class com.pup.PatientInfoView extends Backbone.View
    events:
      'click .save-changes': '_updateModel'

    initialize: (options) =>
      @listenTo @model, 'change:name change:sleep_interval_ms change:sit_interval_ms', @render
      @listenTo @model, 'change:angle', @_renderAngle

    render: =>
      @$el.empty()

      sleepMin = @model.get('sleep_interval_ms') / (60 * 1000)
      sitMin = @model.get('sit_interval_ms') / (60 * 1000)

      source = $('#patient-info-template').html()
      template = Handlebars.compile(source)
      @$el.append template(_.defaults({sleepMin: sleepMin, sitMin: sitMin}, @model.attributes))
      @_renderAngle

    _renderAngle: =>

    _updateModel: =>
      name = @$('.name-input').val()
      sleepMin = @$('.sleep-input').val()
      sitMin = @$('.sit-input').val()

      sleepMs = parseInt(sleepMin) * 60 * 1000
      sitMs = parseInt(sitMin) * 60 * 1000
      @model.set
        name: name
        sleep_interval_ms: sleepMs
        sit_interval_ms: sitMs