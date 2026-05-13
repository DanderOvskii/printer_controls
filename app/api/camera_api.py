from flask import Blueprint, jsonify, request, Response
from flask_login import login_required

from app.camera.camera import camera, video_stream

bp = Blueprint(
    "camera",
    __name__,
    url_prefix="/api/camera"
)


@bp.route("/video_feed", methods=["GET"])
@login_required
def video_feed():
    return Response(
        video_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@bp.route("/switch", methods=["POST"])
@login_required
def switch_camera():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Missing JSON body"
        }), 400

    cam_index = data.get("camera")

    if cam_index is None:
        return jsonify({
            "success": False,
            "error": "Missing 'camera' field"
        }), 400

    try:
        cam_index = int(cam_index)

    except ValueError:
        return jsonify({
            "success": False,
            "error": "Camera index must be an integer"
        }), 400

    try:
        camera.switch_camera(cam_index)

        return jsonify({
            "success": True,
            "camera": cam_index,
            "message": "Camera switched successfully"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
