// create global websocket variable
var websocket;

// send mouse pos
const sendMousePos = (mouseEvent) => {
    websocket.send(JSON.stringify({x:mouseEvent.clientX, y:mouseEvent.clientY}));
    // TODO determine if needs to be screenX/screenY, pageX/pageY for cursors to line up
}

// join cursorparty
const join = (e) => {
    // remove landing page elements
    var partyzone = document.getElementById("partyzone");
    while (partyzone.firstChild) {
        partyzone.removeChild(partyzone.firstChild);
    }

    // update cursor
    partyzone.style.cursor = "url('static/cursor.png') 7 0,default";

    // connect to websocket server
    websocket = new WebSocket("ws://localhost:8081/");

    // add onmessage handler
    websocket.onmessage = ( {data} ) => {
        console.log(data);
    }

    // add onmousemove listener
    partyzone.addEventListener("mousemove", sendMousePos)
}

// when DOM loads, add onclick to join button
window.addEventListener("DOMContentLoaded", () => {
    var joinbutton = document.getElementById("joinbutton");
    joinbutton.addEventListener("click", join);
})