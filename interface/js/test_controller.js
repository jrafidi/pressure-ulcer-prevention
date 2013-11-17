var socket;

window.onload = function () {
  if (!window.WebSocket) {
    console.log("Your browser does not support web sockets!");
    return;
  }

  socket = new WebSocket("ws://localhost:9000/");

  // Receive data from the server
  socket.onmessage = function (evt) {
    console.log(JSON.parse(evt.data))
  };
};