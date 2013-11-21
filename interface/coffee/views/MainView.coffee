do ->
  class com.pup.MainView extends Backbone.View
    initialize: =>
      # no-op

    render: =>
      @$el.empty()
      @listView = new com.pup.PatientListView
        model: @model
      @listView.render()

      @$el.append(@listView.$el)