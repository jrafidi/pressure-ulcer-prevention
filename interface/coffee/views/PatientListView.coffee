do ->
  class com.pup.PatientListView extends Backbone.View
    className: 'patient-list'

    initialize: (options) =>
      @selectionModel = options.selectionModel
      @listenTo @model, 'add remove reset', @render

    render: =>
      @$el.empty()
      for m in @model.models
        listItem = new com.pup.PatientListItem
          model: m
          selectionModel: @selectionModel
        listItem.render()
        @$el.append listItem.$el

  class com.pup.PatientListItem extends Backbone.View
    className: 'patient-item'

    events:
      'click': '_selectModel'

    initialize: (options) =>
      @selectionModel = options.selectionModel
      @listenTo @model, 'change:name', @render
      @listenTo @selectionModel, 'change', @render

    render: =>
      @$el.empty()
      source = $('#patient-item-template').html()
      template = Handlebars.compile(source)
      @$el.append template(@model.attributes)

      if @selectionModel.get('selected') == @model.cid
        @$el.addClass('selected')
      else
        @$el.removeClass('selected')

    _selectModel: =>
      @selectionModel.set('selected', @model.cid)