do ->
  class com.pup.PatientContentView extends Backbone.View
    className: 'patient-content'

    initialize: (options) =>
      @selectionModel = options.selectionModel

      @listenTo @selectionModel, 'change', @render

    render: =>
      @$el.empty()
      
      if !@selectionModel.get('selected')?
        @$el.append $('<div class="nothing"/>').text('Select a patient on the left.')
      else
        @$el.append $('<div class="nothing"/>').text('Selected.')