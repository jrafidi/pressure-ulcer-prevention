com.pup.WEBSOCKET_PORT = '8000'

$('document').ready ( =>
  # Create the data model (collection of patients)
  patientModels = new Backbone.Collection()
  patientModels.model = com.pup.PatientModel

  # Make the controller, which will sync model data on connection
  patientController = new com.pup.PatientController
    model: patientModels

  # Draw the main view
  mainView = new com.pup.MainView
    model: patientModels
    el: $('body')
  mainView.render()
)