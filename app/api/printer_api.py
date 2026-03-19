from flask import Blueprint, jsonify, request
from app.printer.printer_service import PrinterService

bp = Blueprint("printer", __name__, url_prefix="/api/printer")
printer_service = PrinterService()

@bp.route("/enqueue", methods=["POST"])
def enqueue():
    data = request.json
    commands = data.get("commands")
    if not commands:
        return jsonify({"error": "No commands provided"}), 400

    if isinstance(commands, str):
        commands = [commands]

    responses = []
    for cmd in commands:
        responses.append(printer_service.enqueue_command(cmd))

    return jsonify({"status": "queued", "commands": commands, "responses": responses})

@bp.route("/status")
def status():
    return jsonify(printer_service.get_state())
