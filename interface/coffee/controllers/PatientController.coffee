do ->
  class com.pup.PatientController
    constructor: (options) ->
      $.extend @, Backbone.Events

      @model = options.model
      @selectionModel = options.selectionModel

      @_initializeSocket()

      @listenTo @model, 'change', @_updateSettings

    _initializeSocket: =>
      @socket = new WebSocket("ws://#{com.pup.WEBSOCKET_URL}:#{com.pup.WEBSOCKET_PORT}/")
      @socket.onmessage = @_parseMessage

    _parseMessage: (message) =>
      data = JSON.parse(message.data)
      if data.type == 'state'
        delete data['type']

        ids = []
        for deviceId, info of data
          ids.push(deviceId)
          if @model.where({'deviceId': parseInt(deviceId)}).length == 0
            @model.add(new com.pup.PatientModel(info.attributes))

        for m in @model.models
          if !_.contains(ids, m.get('deviceId').toString())
            @model.remove(m)

            if @selectionModel.get('selected') == m.cid
              @selectionModel.set('selected', null)
      else if data.type == 'update'
        device = @model.where({'deviceId': data.deviceId})[0]
        device.set('angle', data.angle)
        device.set('sleeping', data.sleeping)
      else if data.type == 'turn'
        device = @model.where({'deviceId': data.deviceId})[0]
        turns = device.get('turns')
        turns.push(data.turn)
        device.set('turns', turns)

    _updateSettings: (patient) =>
      @_sendMessage(patient.attributes)

    _sendMessage: (data) =>
      msg = JSON.stringify(data)
      @socket.send(msg)