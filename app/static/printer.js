
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

function pollPrinterState() {
    fetch("/api/printer/status")
        .then(response => response.json())
        .then(data => {
            document.getElementById("status").textContent = JSON.stringify(data.state, null, 2);
        });
}

setInterval(pollPrinterState, 2000);

function pollprinterTemp(){
    response = sendCommand("M105");
    for (const line of response) {        
        if (line.startsWith("ok T:")) {
            const noztemp = line.split("T:")[1].split(" ")[0];
            const bedtemp = line.split("B:")[1].split(" ")[0];
            document.getElementById("bedtemperature").textContent = bedtemp + "°C";
            document.getElementById("temperature").textContent = noztemp + "°C";
            break;
        }
}
}
setInterval(pollprinterTemp, 5000);


async function reconnect_printer() {
    try{
          const res = await fetch("/api/printer/connect", {
            method: "GET",
           
        });

        const data = await res.json();
        set_response(data);
        updatePrinterState()
    }catch (error){
        console.error("Error:",error);
    }
    
}

function stopPrinter() {
  let text = "Press a button!\nEither OK or Cancel.";
  if (confirm(text) == true) {
    sendCommand("M0");
  } else {
    alert("Command cancelled");
  }
}