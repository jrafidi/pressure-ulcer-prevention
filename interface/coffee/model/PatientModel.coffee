do ->
  class com.pup.PatientModel extends Backbone.Model
    defaults: =>
      id: null
      name: ''
      notes: ''

      sleep_interval_ms: 7200000
      sit_interval_ms: 900000

      angle: 0
      past_turns: []