from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    is_verified  = db.Column(db.Boolean, default=False)
    verify_token = db.Column(db.String(64), unique=True, nullable=True)

    reset_token        = db.Column(db.String(64), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_verify_token(self):
        self.verify_token = secrets.token_urlsafe(32)
        return self.verify_token

    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token

    def is_reset_token_valid(self):
        return self.reset_token_expiry and datetime.utcnow() < self.reset_token_expiry


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class HeroContent(db.Model):
    __tablename__ = 'hero_content'
    id         = db.Column(db.Integer, primary_key=True)
    badge_text = db.Column(db.String(100), default='Information Systems Student')
    heading    = db.Column(db.String(200), default='get to know me')
    photo_url  = db.Column(db.String(500))
    mini_title = db.Column(db.String(100), default='My Current Favorite')
    mini_sub   = db.Column(db.String(100), default='My Lovely Boyfriend')
    mini_item1_label = db.Column(db.String(100), default='Kopi Banjar Secerca')
    mini_item1_value = db.Column(db.String(100), default='5/5')
    mini_item2_label = db.Column(db.String(100), default='Sunset Sky')
    mini_item2_value = db.Column(db.String(100), default="God's Creation")


class AboutContent(db.Model):
    __tablename__ = 'about_content'
    id          = db.Column(db.Integer, primary_key=True)
    heading     = db.Column(db.String(200), default='The Human Who Loves Database')
    description = db.Column(db.Text)
    playlist_item1_name = db.Column(db.String(100), default='Memabsuh')
    playlist_item1_sub  = db.Column(db.String(100), default='Hindia')
    playlist_item2_name = db.Column(db.String(100), default='Wonderwall')
    playlist_item2_sub  = db.Column(db.String(100), default='Oasis')
    spotify_url = db.Column(db.String(500))


class Skill(db.Model):
    __tablename__ = 'skills'
    id         = db.Column(db.Integer, primary_key=True)
    category   = db.Column(db.String(50))   # 'hard', 'soft', 'tool'
    name       = db.Column(db.String(100), nullable=False)
    level      = db.Column(db.Integer)       # untuk mastery bar (0-100), NULL jika tag biasa
    icon       = db.Column(db.String(10))    # emoji untuk tool
    order      = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Experience(db.Model):
    __tablename__ = 'experiences'
    id          = db.Column(db.Integer, primary_key=True)
    year        = db.Column(db.String(20), nullable=False)
    role        = db.Column(db.String(200), nullable=False)
    company     = db.Column(db.String(200))
    description = db.Column(db.Text)
    order       = db.Column(db.Integer, default=0)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class Project(db.Model):
    __tablename__ = 'projects'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url   = db.Column(db.String(500))
    tags        = db.Column(db.String(300))   # disimpan sebagai "Figma,UI/UX"
    link        = db.Column(db.String(500))
    order       = db.Column(db.Integer, default=0)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(200), nullable=False)
    message    = db.Column(db.Text, nullable=False)
    is_read    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)