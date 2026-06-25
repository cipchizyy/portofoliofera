import os
import resend

resend.api_key = os.getenv('RESEND_API_KEY')

# Selama domain kamu sendiri belum diverifikasi di Resend, gunakan
# alamat default ini — Resend tetap mengizinkan kirim email untuk testing.
FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
APP_BASE_URL = os.getenv('APP_BASE_URL', 'http://127.0.0.1:5000')

# Email tujuan saat ada pesan baru dari form contact portfolio.
# Ganti dengan email kamu sendiri lewat .env (ADMIN_NOTIFICATION_EMAIL).
ADMIN_EMAIL = os.getenv('ADMIN_NOTIFICATION_EMAIL', os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev'))


def send_contact_notification(name, email, message):
    """Kirim notifikasi ke admin saat ada pesan baru dari form contact publik."""
    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": ADMIN_EMAIL,
            "subject": f"Pesan Baru dari {name} — Portfolio",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
                    <h2 style="color:#111;">📬 Pesan Baru Masuk</h2>
                    <p style="color:#444; font-size:14px; line-height:1.6;">
                        <strong>Nama:</strong> {name}<br/>
                        <strong>Email:</strong> {email}
                    </p>
                    <div style="background:#f3f4f6; border-radius:10px; padding:14px; margin-top:12px;">
                        <p style="color:#333; font-size:14px; line-height:1.6; margin:0;">{message}</p>
                    </div>
                    <p style="color:#888; font-size:12px; margin-top:20px;">
                        Buka panel admin untuk membalas atau menandai pesan ini sebagai dibaca.
                    </p>
                </div>
            """
        })
        return True
    except Exception as e:
        print(f"Gagal mengirim notifikasi contact: {e}")
        return False


def send_verification_email(to_email, username, token):
    verify_url = f"{APP_BASE_URL}/auth/verify-email/{token}"
    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": to_email,
            "subject": "Verifikasi Akun Portfolio Kamu",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
                    <h2 style="color:#111;">Halo, {username} 👋</h2>
                    <p style="color:#444; font-size:14px; line-height:1.6;">
                        Terima kasih sudah mendaftar. Klik tombol di bawah untuk memverifikasi email kamu.
                    </p>
                    <a href="{verify_url}"
                       style="display:inline-block; background:#111; color:#fff; padding:12px 24px;
                              border-radius:30px; text-decoration:none; font-weight:600; margin-top:12px;">
                        Verifikasi Email
                    </a>
                    <p style="color:#888; font-size:12px; margin-top:20px;">
                        Kalau kamu tidak mendaftar, abaikan email ini.
                    </p>
                </div>
            """
        })
        return True
    except Exception as e:
        print(f"Gagal mengirim email verifikasi: {e}")
        return False


def send_reset_password_email(to_email, username, token):
    reset_url = f"{APP_BASE_URL}/auth/reset-password/{token}"
    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": to_email,
            "subject": "Reset Password Akun Portfolio Kamu",
            "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
                    <h2 style="color:#111;">Halo, {username}</h2>
                    <p style="color:#444; font-size:14px; line-height:1.6;">
                        Kami menerima permintaan reset password untuk akun kamu.
                        Klik tombol di bawah untuk membuat password baru. Link ini berlaku 1 jam.
                    </p>
                    <a href="{reset_url}"
                       style="display:inline-block; background:#111; color:#fff; padding:12px 24px;
                              border-radius:30px; text-decoration:none; font-weight:600; margin-top:12px;">
                        Reset Password
                    </a>
                    <p style="color:#888; font-size:12px; margin-top:20px;">
                        Kalau kamu tidak meminta ini, abaikan email ini — password kamu tetap aman.
                    </p>
                </div>
            """
        })
        return True
    except Exception as e:
        print(f"Gagal mengirim email reset password: {e}")
        return False