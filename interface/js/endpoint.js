(function() {
  var _this = this;

  $('document').ready((function() {
    var mainView, patientController, patientModels;
    patientModels = new Backbone.Collection();
    patientModels.model = com.pup.PatientModel;
    patientController = new com.pup.PatientController({
      model: patientModels
    });
    mainView = new com.pup.MainView({
      model: patientModels,
      el: $('body')
    });
    return mainView.render();
  }));

}).call(this);
