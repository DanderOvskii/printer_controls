from flask import Blueprint, jsonify, request, Response
from app.camera.camera import video_stream, switch_camera
from flask_login import login_required

bp = Blueprint("camera",__name__,url_prefix="/api/camera")

@bp.route("/video_feed",methods = ["GET", "POST"])
@login_required
def video_feed():
    return Response(video_stream(), mimetype= 'multipart/x-mixed-replace; boundary=frame')

@bp.route('/switch_camera',methods = ["GET", "POST"])
@login_required
def switch():
    cam_index = int(request.args.get('cam'))
    switch_camera(cam_index)
    return "Camera switched"
