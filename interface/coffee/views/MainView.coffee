do ->
  class com.pup.MainView extends Backbone.View
    initialize: (options) =>
      @selectionModel = options.selectionModel

    render: =>
      @$el.empty()
      source = $('#top-bar-template').html()
      template = Handlebars.compile(source)
      @$el.append template({})

      @listView = new com.pup.PatientListView
        model: @model
        selectionModel: @selectionModel
      @listView.render()

      @contentView = new com.pup.PatientContentView
        model: @model
        selectionModel: @selectionModel
      @contentView.render()

      @$el.append(@listView.$el)
      @$el.append(@contentView.$el)