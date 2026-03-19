
function set_response(data){
	console.log("update responmse")
    document.getElementById("response").textContent = JSON.stringify(data, null, 2);
}

async function sendCommand(commands) {
    try {
        const body = Array.isArray(commands) ? commands : [commands];
        const res = await fetch("/api/printer/enqueue", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ commands: body })
        });

        const data = await res.json();
        set_response(data);
        updatePrinterState();
    } catch (error) {
        console.error("Error:", error);
    }
}

async function updatePrinterState(){
    try{
        const res = await fetch("/api/printer/status", {
            method: "GET",
           
        });
        const data = await res.json();
        document.getElementById("status").textContent = JSON.stringify(data, null, 2);
    }catch (error) {
        console.error("Error:", error);
    }
}
