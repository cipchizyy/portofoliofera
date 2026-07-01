from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from models import Admin
from services.resend_service import send_verification_email, send_reset_password_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            if not admin.is_verified:
                flash('Email kamu belum diverifikasi. Cek inbox kamu untuk link verifikasi.', 'error')
                return render_template('admin/login.html')
            login_user(admin)
            return redirect(url_for('admin.dashboard'))

        flash('Username atau password salah.', 'error')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('Semua field wajib diisi.', 'error')
            return render_template('admin/register.html')

        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'error')
            return render_template('admin/register.html')

        if len(password) < 8:
            flash('Password minimal 8 karakter.', 'error')
            return render_template('admin/register.html')

        if Admin.query.filter_by(username=username).first():
            flash('Username sudah digunakan.', 'error')
            return render_template('admin/register.html')

        if Admin.query.filter_by(email=email).first():
            flash('Email sudah terdaftar.', 'error')
            return render_template('admin/register.html')

        admin = Admin(
            username=username,
            email=email,
            password=generate_password_hash(password),
            is_verified=False
        )
        token = admin.generate_verify_token()
        db.session.add(admin)
        db.session.commit()

        email_sent = send_verification_email(email, username, token)
        if email_sent:
            flash('Akun berhasil dibuat! Cek email kamu untuk verifikasi sebelum login.', 'success')
        else:
            flash('Akun dibuat, tapi gagal mengirim email verifikasi. Hubungi admin.', 'error')

        return redirect(url_for('auth.login'))

    return render_template('admin/register.html')


@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    admin = Admin.query.filter_by(verify_token=token).first()

    if not admin:
        flash('Link verifikasi tidak valid atau sudah digunakan.', 'error')
        return redirect(url_for('auth.login'))

    admin.is_verified = True
    admin.verify_token = None
    db.session.commit()

    flash('Email berhasil diverifikasi! Silakan login.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        admin = Admin.query.filter_by(email=email).first()

        if admin:
            token = admin.generate_reset_token()
            db.session.commit()
            send_reset_password_email(admin.email, admin.username, token)

        flash('Kalau email kamu terdaftar, link reset password sudah dikirim. Cek inbox kamu.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('admin/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    admin = Admin.query.filter_by(reset_token=token).first()

    if not admin or not admin.is_reset_token_valid():
        flash('Link reset password tidak valid atau sudah kedaluwarsa.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'error')
            return render_template('admin/reset_password.html', token=token)

        if len(password) < 8:
            flash('Password minimal 8 karakter.', 'error')
            return render_template('admin/reset_password.html', token=token)

        admin.password = generate_password_hash(password)
        admin.reset_token = None
        admin.reset_token_expiry = None
        db.session.commit()

        flash('Password berhasil diubah! Silakan login dengan password baru.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('admin/reset_password.html', token=token)