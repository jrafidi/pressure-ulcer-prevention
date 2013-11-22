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
        source = $('#patient-content-template').html()
        template = Handlebars.compile(source)
        @$el.append template({})

        cid = @selectionModel.get('selected')
        patient = @model.get(cid)

        @infoView = new com.pup.PatientInfoView
          model: patient
          el: @$('.patient-content-top')
        @infoView.render()