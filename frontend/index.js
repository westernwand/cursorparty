function join() {
    var partyzone = document.getElementById("partyzone")
    
    while (partyzone.firstChild) {
        partyzone.removeChild(partyzone.firstChild)
    }

    partyzone.style.cursor = "url('static/cursor.png') 7 0,default"
}