// create global websocket variable
var websocket;

// send mouse pos
const sendMousePos = (mouseEvent) => {
    var x = mouseEvent.clientX / window.innerWidth;
    var y = mouseEvent.clientY / window.innerHeight;
    websocket.send(JSON.stringify( {"x":x, "y":y} ));
}

// join cursorparty
const join = (e) => {
    // remove landing page elements
    var partyzone = document.getElementById("partyzone");
    while (partyzone.firstChild) {
        partyzone.removeChild(partyzone.firstChild);
    }

    // update cursor
    document.body.style.cursor = "url('static/cursor.png') 7 0, default";

    // connect to websocket server
    websocket = new WebSocket("ws://localhost:8081/");

    // add onmessage handler
    websocket.onmessage = ( {data} ) => {
        console.log(data);
    }
    websocket.onclose = () => {
        // TODO add visual stating that connection has closed
        console.log("connection closed");
    }

    // add onmousemove listener
    partyzone.addEventListener("mousemove", sendMousePos);
}

// when DOM loads, add onclick to join button
window.addEventListener("DOMContentLoaded", () => {
    var joinbutton = document.getElementById("joinbutton");
    joinbutton.addEventListener("click", join);
})