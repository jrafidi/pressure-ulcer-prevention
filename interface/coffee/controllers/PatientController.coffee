do ->
  class com.pup.PatientController
    constructor: (options) ->
      $.extend @, Backbone.Events

      @model = options.model

      @_initializeSocket()

    _initializeSocket: =>
      @socket = new WebSocket("ws://localhost:9000/")
      @socket.onmessage = @_parseMessage

    _parseMessage: (message) =>
      # Switch on the message type

    _sendMessage: (data) =>
      msg = JSON.stringify(data)
      @socket.send(msg)