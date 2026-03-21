let camInt = 1;
function toggleCam() {
console.log("swich")
camInt = (camInt === 1) ? 4:1;
switchCam(camInt);
}

function switchCam(cam) {
    fetch(`api/camera/switch_camera?cam=${cam}`)
        .then(() => {
            // Force reload the camera feed by updating the src with a cache buster
            const img = document.getElementById('bg');
            const baseUrl = img.src.split('?')[0];
            img.src = baseUrl + '?t=' + new Date().getTime();
        });
}
