var websocket;
var cursor_count;

// send mouse pos
const sendMousePos = (mouseEvent) => {
    var x = mouseEvent.clientX / window.innerWidth;
    var y = mouseEvent.clientY / window.innerHeight;
    websocket.send(JSON.stringify( {"x":x, "y":y} ));
}

const handleMessage = ( {data} ) => {
    json_data = JSON.parse(data)
    console.log(json_data);
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

    websocket.onmessage = handleMessage

    websocket.onclose = (event) => {
        console.log("connection closed");
        if (event.code == 4001) {
            if (!confirm("There are too many people in the party right now, try again later!\nDo you want to have a private party?")) {
                window.location.reload()
            }
        }
    }

    // add onmousemove listener
    partyzone.addEventListener("mousemove", sendMousePos);
}

// when DOM loads, add onclick to join button
window.addEventListener("DOMContentLoaded", () => {
    var joinbutton = document.getElementById("joinbutton");
    joinbutton.addEventListener("click", join);
})