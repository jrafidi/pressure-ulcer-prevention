com.pup.WEBSOCKET_URL = window.location.origin.split('//')[1].split(':')[0]
com.pup.WEBSOCKET_PORT = '8000'

$('document').ready ( =>
  # Create the data model (collection of patients)
  patientModels = new Backbone.Collection()
  patientModels.model = com.pup.PatientModel

  # Create the selection model
  selectionModel = new Backbone.Model
    selected: null

  # Make the controller, which will sync model data on connection
  patientController = new com.pup.PatientController
    model: patientModels
    selectionModel: selectionModel

  # Draw the main view
  mainView = new com.pup.MainView
    model: patientModels
    selectionModel: selectionModel
    el: $('body')
  mainView.render()
)