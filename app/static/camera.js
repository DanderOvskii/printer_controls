function switchCam(cam) {
    fetch(`api/camera/switch_camera?cam=${cam}`);
}
