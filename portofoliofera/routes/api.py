from flask import Blueprint, request, jsonify
from extensions import db
from models import ContactMessage
from services.resend_service import send_contact_notification

api_bp = Blueprint('api', __name__)


@api_bp.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name    = (data.get('name') or '').strip()
    email   = (data.get('email') or '').strip()
    message = (data.get('message') or '').strip()

    if not name or not email or not message:
        return jsonify({'success': False, 'error': 'Semua field wajib diisi.'}), 400

    # Simpan ke database
    msg = ContactMessage(name=name, email=email, message=message)
    db.session.add(msg)
    db.session.commit()

    # Kirim email notifikasi
    send_contact_notification(name, email, message)

    return jsonify({'success': True, 'message': 'Pesan berhasil dikirim!'})