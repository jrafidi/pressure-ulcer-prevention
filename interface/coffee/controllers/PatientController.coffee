do ->
  class com.pup.PatientController
    constructor: (options) ->
      $.extend @, Backbone.Events

      @model = options.model

      @_initializeSocket()

    _initializeSocket: =>
      @socket = new WebSocket("ws://localhost:#{com.pup.WEBSOCKET_PORT}/")
      @socket.onmessage = @_parseMessage

    _parseMessage: (message) =>
      data = JSON.parse(message.data)
      if data.type == 'state'
        delete data['type']

        ids = []
        for deviceId, info of data
          ids.push(deviceId)
          if @model.where({'deviceId': deviceId}).length == 0
            @model.add(new com.pup.PatientModel(info.attributes))

        for m in @model.models
          if !_.contains(ids, m.get('deviceId').toString())
            @model.remove(m)

        console.log @model.models

    _sendMessage: (data) =>
      msg = JSON.stringify(data)
      @socket.send(msg)