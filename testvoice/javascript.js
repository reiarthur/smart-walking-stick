// Create a client instance
var port = 37599;
client = new Paho.MQTT.Client("tailor.cloudmqtt.com", port, "client_id");
//Example client = new Paho.MQTT.Client("m11.cloudmqtt.com", 32903, "web_" + parseInt(Math.random() * 100, 10));

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;
var options = {
    useSSL: true,
    userName: "test",
    password: "1234",
    onSuccess: onConnect,
    onFailure: doFail
}

// connect the client
client.connect(options);

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    console.log("onConnect");
    client.subscribe("audio/objects");
}

function doFail(e) {
    console.log(e);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:" + responseObject.errorMessage);
    }
}

// called when a message arrives
function onMessageArrived(message) {
    //console.log("onMessageArrived:" + message.payloadString);

    responsiveVoice.speak(message.payloadString);
}