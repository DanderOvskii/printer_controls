from flask import Blueprint, jsonify, request, Response
from flask_login import login_required

from app.camera.camera import camera, video_stream

bp = Blueprint(
    "camera",
    __name__,
    url_prefix="/api/camera"
)


@bp.route("/video_feed", methods=["GET"])
def video_feed():
    return Response(
        video_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )



@bp.route('/switch',methods = ["GET"])
def switch():
    cam_index = int(request.args.get('cam'))
    camera.switch_camera(cam_index)
    return "Camera switched"