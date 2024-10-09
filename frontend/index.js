// websocket connecting back to server
var websocket;

// partyzone div
var partyzone;

// map existing cursors
var cursors = new Map();

class Cursor {
    constructor(id) {
        this.id = id;
        // create new cursor image
        this.img = document.createElement('img');
        this.img.src = 'static/cursor.png';
        this.img.class = 'cursor';
        partyzone.appendChild(this.img);
    }

    update_pos(x, y) {
        this.x = x;
        this.y = y;
    }

    move() {
        // move cursor on screen
        this.img.style.marginLeft = String(this.x * window.innerWidth) + 'px';
        this.img.style.marginTop = String(this.y * window.innerHeight) + 'px';
    }

    remove() {
        // remove cursor image
        this.img.remove()
    }
}

// send mouse pos
const sendMousePos = (mouseEvent) => {
    var x = mouseEvent.clientX / window.innerWidth;
    var y = mouseEvent.clientY / window.innerHeight;
    websocket.send(JSON.stringify( {"x":x, "y":y} ));
}

const handleMessage = ( message ) => {
    var cursor = cursors.get(message.id);
    if (message.type === 'update') {
        if (cursor === undefined) {
            // add new cursor to cursors
            cursor = new Cursor(message.id);
            cursors.set(message.id, cursor);
        }
        cursor.update_pos(message.x, message.y);
        cursor.move();

    } else if (message.type === 'remove' && cursor !== undefined) {
        cursor.remove();
        cursors.delete(message.id);
    }
}

// join cursorparty
const join = (e) => {
    // remove landing page elements
    partyzone = document.getElementById("partyzone");
    while (partyzone.firstChild) {
        partyzone.removeChild(partyzone.firstChild);
    }

    // update cursor
    document.body.style.cursor = "url('static/cursor.png') 7 0, default";

    // connect to websocket server
    websocket = new WebSocket("ws://localhost:8081/");

    websocket.onmessage = ( {data} ) => {
        var json_data = JSON.parse(data);
        console.log(json_data);
        handleMessage(json_data);
    }

    websocket.onclose = (event) => {
        console.log("connection closed");
        if (event.code == 4001) {
            if (!confirm("There are too many people in the party right now, try again later!\nDo you want to have a private party?")) {
                window.location.reload();
            }
        }
    }

    partyzone.addEventListener("mousemove", sendMousePos);
}

// when DOM loads, add onclick to join button
window.addEventListener("DOMContentLoaded", () => {
    var joinbutton = document.getElementById("joinbutton");
    joinbutton.addEventListener("click", join);
});

// TODO move cursors as window is resized
// window.addEventListener("resize", () => {
//     for (let i = 0; i < cursors.size; i++) {
//         cursors.
//     }
// });