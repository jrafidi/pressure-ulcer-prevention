do ->
  class com.pup.PatientModel extends Backbone.Model
    defaults: =>
      deviceId: null
      name: ''
      notes: ''

      sleep_interval_ms: 7200000
      sit_interval_ms: 900000

      angle: 0
      sleeping: true
      turns: []