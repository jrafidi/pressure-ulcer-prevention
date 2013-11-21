do ->
  class com.pup.PatientListView extends Backbone.View
    className: 'patient-list'

    initialize: =>
      @listenTo @model, 'add remove reset change:name', @render

    render: =>
      @$el.empty()
      for model in @model.models
        source = $('#patient-item-template').html()
        template = Handlebars.compile(source)
        @$el.append template(model.attributes)