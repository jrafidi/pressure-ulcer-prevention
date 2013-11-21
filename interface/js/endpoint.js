(function() {
  var _this = this;

  com.pup.WEBSOCKET_PORT = '8000';

  $('document').ready((function() {
    var mainView, patientController, patientModels, selectionModel;
    patientModels = new Backbone.Collection();
    patientModels.model = com.pup.PatientModel;
    selectionModel = new Backbone.Model({
      selected: null
    });
    patientController = new com.pup.PatientController({
      model: patientModels,
      selectionModel: selectionModel
    });
    mainView = new com.pup.MainView({
      model: patientModels,
      selectionModel: selectionModel,
      el: $('body')
    });
    return mainView.render();
  }));

}).call(this);
