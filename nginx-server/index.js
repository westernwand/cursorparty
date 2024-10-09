// file location for cursor png
const USER_CURSOR_FILE = 'static/cursor.png';
const OTHER_CURSOR_FILE = 'static/cursor_gray.png';
// pixel offsets for locating the "point" of the cursor png
const CURSOR_X_OFFSET = 7;
const CURSOR_Y_OFFSET = 0;
// dimensions of cursor png
const CURSOR_WIDTH = 31;
const CURSOR_HEIGHT = 38;

// websocket connecting back to server
var websocket;

// partyzone div
var partyzone;

// map for other users' cursors
var cursors = new Map();

// class containing another user's cursor metadata
class Cursor {
    constructor(id) {
        this.id = id;
        // create new cursor image
        this.img = document.createElement('img');
        this.img.src = OTHER_CURSOR_FILE;
        this.img.className = 'cursor';
        partyzone.appendChild(this.img);
    }

    update_pos(x, y) {
        this.x = x;
        this.y = y;
    }

    move() {
        // move cursor on screen
        var clientX = Math.floor(this.x * window.innerWidth);
        var clientY = Math.floor(this.y * window.innerHeight);

        var xPartyzone = clientX - partyzone.getBoundingClientRect().x - CURSOR_X_OFFSET;
        var yPartyzone = clientY - partyzone.getBoundingClientRect().y - CURSOR_Y_OFFSET;

        this.img.style.left = String(xPartyzone) + 'px';
        this.img.style.top = String(yPartyzone) + 'px';
    }

    remove() {
        // remove cursor image
        this.img.remove()
    }
}

// send mouse pos
const sendMousePos = (mouseEvent) => {
    var x = (mouseEvent.clientX) / window.innerWidth;
    var y = (mouseEvent.clientY) / window.innerHeight;
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

    // update user cursor style
    document.body.style.cursor = "url(" + USER_CURSOR_FILE + ") " + String(CURSOR_X_OFFSET) + " " + String(CURSOR_Y_OFFSET) + ", default";

    // connect to websocket server
    websocket = new WebSocket("ws://localhost:8080/party");

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
