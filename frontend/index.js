const join = () => {
    // remove landing page elements
    var partyzone = document.getElementById("partyzone");
    while (partyzone.firstChild) {
        partyzone.removeChild(partyzone.firstChild);
    }

    // update cursor
    partyzone.style.cursor = "url('static/cursor.png') 7 0,default";

    // connect to websocket server
    const websocket = new WebSocket("ws://localhost:8081/");
    websocket.onmessage = ( {data} ) => {
        console.log(data)
    }
}