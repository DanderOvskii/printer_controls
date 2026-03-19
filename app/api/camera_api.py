from flask import Blueprint, jsonify, request, Response
from app.camera.camera import video_stream

bp = Blueprint("camera",__name__,url_prefix="/api/camera")

@bp.route("/video_feed",methods = ["GET", "POST"])
def video_feed():
    return Response(video_stream(), mimetype= 'multipart/x-mixed-replace; boundary=frame')
