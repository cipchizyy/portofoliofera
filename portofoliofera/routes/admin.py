from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from extensions import db
from models import HeroContent, AboutContent, Skill, Experience, Project, ContactMessage
from services.cloudinary_service import upload_image, delete_image, get_public_id

admin_bp = Blueprint('admin', __name__)


# ── DASHBOARD ──
@admin_bp.route('/')
@login_required
def dashboard():
    stats = {
        'skills':      Skill.query.count(),
        'experiences': Experience.query.count(),
        'projects':    Project.query.count(),
        'messages':    ContactMessage.query.count(),
        'unread':      ContactMessage.query.filter_by(is_read=False).count(),
    }
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_messages=recent_messages)


# ════════════════════════════════════════
# ── HERO ──
# ════════════════════════════════════════
@admin_bp.route('/hero', methods=['GET', 'POST'])
@login_required
def hero():
    hero = HeroContent.query.first() or HeroContent()
    if request.method == 'POST':
        hero.badge_text       = request.form.get('badge_text', '')
        hero.heading          = request.form.get('heading', '')
        hero.mini_title       = request.form.get('mini_title', '')
        hero.mini_sub         = request.form.get('mini_sub', '')
        hero.mini_item1_label = request.form.get('mini_item1_label', '')
        hero.mini_item1_value = request.form.get('mini_item1_value', '')
        hero.mini_item2_label = request.form.get('mini_item2_label', '')
        hero.mini_item2_value = request.form.get('mini_item2_value', '')

        photo = request.files.get('photo')
        if photo and photo.filename:
            if hero.photo_url:
                delete_image(get_public_id(hero.photo_url))
            hero.photo_url = upload_image(photo, folder='portfolio/hero')

        if not hero.id:
            db.session.add(hero)
        db.session.commit()
        flash('Hero section berhasil diperbarui!', 'success')
        return redirect(url_for('admin.hero'))
    return render_template('admin/hero.html', hero=hero)


# ════════════════════════════════════════
# ── ABOUT ──
# ════════════════════════════════════════
@admin_bp.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    about = AboutContent.query.first() or AboutContent()
    if request.method == 'POST':
        about.heading             = request.form.get('heading', '')
        about.description         = request.form.get('description', '')
        about.playlist_item1_name = request.form.get('playlist_item1_name', '')
        about.playlist_item1_sub  = request.form.get('playlist_item1_sub', '')
        about.playlist_item2_name = request.form.get('playlist_item2_name', '')
        about.playlist_item2_sub  = request.form.get('playlist_item2_sub', '')
        about.spotify_url         = request.form.get('spotify_url', '')

        if not about.id:
            db.session.add(about)
        db.session.commit()
        flash('About section berhasil diperbarui!', 'success')
        return redirect(url_for('admin.about'))
    return render_template('admin/about.html', about=about)


# ════════════════════════════════════════
# ── SKILLS ──
# ════════════════════════════════════════
@admin_bp.route('/skills')
@login_required
def skills():
    all_skills = Skill.query.order_by(Skill.category, Skill.order).all()
    return render_template('admin/skills.html', skills=all_skills)


@admin_bp.route('/skills/add', methods=['POST'])
@login_required
def skill_add():
    skill = Skill(
        category=request.form.get('category'),
        name=request.form.get('name'),
        level=request.form.get('level') or None,
        icon=request.form.get('icon', ''),
        order=int(request.form.get('order', 0))
    )
    db.session.add(skill)
    db.session.commit()
    flash('Skill berhasil ditambahkan!', 'success')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/skills/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def skill_edit(id):
    skill = Skill.query.get_or_404(id)
    if request.method == 'POST':
        skill.category = request.form.get('category')
        skill.name     = request.form.get('name')
        skill.level    = request.form.get('level') or None
        skill.icon     = request.form.get('icon', '')
        skill.order    = int(request.form.get('order', 0))
        db.session.commit()
        flash('Skill berhasil diperbarui!', 'success')
        return redirect(url_for('admin.skills'))
    return render_template('admin/skill_form.html', skill=skill)


@admin_bp.route('/skills/delete/<int:id>', methods=['POST'])
@login_required
def skill_delete(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill berhasil dihapus.', 'success')
    return redirect(url_for('admin.skills'))


# ════════════════════════════════════════
# ── EXPERIENCE ──
# ════════════════════════════════════════
@admin_bp.route('/experiences')
@login_required
def experiences():
    exps = Experience.query.order_by(Experience.order, Experience.created_at.desc()).all()
    return render_template('admin/experiences.html', experiences=exps)


@admin_bp.route('/experiences/add', methods=['GET', 'POST'])
@login_required
def experience_add():
    if request.method == 'POST':
        exp = Experience(
            year=request.form.get('year'),
            role=request.form.get('role'),
            company=request.form.get('company'),
            description=request.form.get('description'),
            order=int(request.form.get('order', 0))
        )
        db.session.add(exp)
        db.session.commit()
        flash('Experience berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.experiences'))
    return render_template('admin/experience_form.html', exp=None)


@admin_bp.route('/experiences/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def experience_edit(id):
    exp = Experience.query.get_or_404(id)
    if request.method == 'POST':
        exp.year        = request.form.get('year')
        exp.role        = request.form.get('role')
        exp.company     = request.form.get('company')
        exp.description = request.form.get('description')
        exp.order       = int(request.form.get('order', 0))
        db.session.commit()
        flash('Experience berhasil diperbarui!', 'success')
        return redirect(url_for('admin.experiences'))
    return render_template('admin/experience_form.html', exp=exp)


@admin_bp.route('/experiences/delete/<int:id>', methods=['POST'])
@login_required
def experience_delete(id):
    exp = Experience.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    flash('Experience berhasil dihapus.', 'success')
    return redirect(url_for('admin.experiences'))


# ════════════════════════════════════════
# ── PROJECTS ──
# ════════════════════════════════════════
@admin_bp.route('/projects')
@login_required
def projects():
    projs = Project.query.order_by(Project.order, Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projs)


@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
def project_add():
    if request.method == 'POST':
        image_url = None
        image = request.files.get('image')
        if image and image.filename:
            image_url = upload_image(image, folder='portfolio/projects')

        proj = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            image_url=image_url,
            tags=request.form.get('tags'),
            link=request.form.get('link'),
            order=int(request.form.get('order', 0))
        )
        db.session.add(proj)
        db.session.commit()
        flash('Project berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', proj=None)


@admin_bp.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def project_edit(id):
    proj = Project.query.get_or_404(id)
    if request.method == 'POST':
        proj.title       = request.form.get('title')
        proj.description = request.form.get('description')
        proj.tags        = request.form.get('tags')
        proj.link        = request.form.get('link')
        proj.order       = int(request.form.get('order', 0))

        image = request.files.get('image')
        if image and image.filename:
            if proj.image_url:
                delete_image(get_public_id(proj.image_url))
            proj.image_url = upload_image(image, folder='portfolio/projects')

        db.session.commit()
        flash('Project berhasil diperbarui!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', proj=proj)


@admin_bp.route('/projects/delete/<int:id>', methods=['POST'])
@login_required
def project_delete(id):
    proj = Project.query.get_or_404(id)
    if proj.image_url:
        delete_image(get_public_id(proj.image_url))
    db.session.delete(proj)
    db.session.commit()
    flash('Project berhasil dihapus.', 'success')
    return redirect(url_for('admin.projects'))


# ════════════════════════════════════════
# ── MESSAGES ──
# ════════════════════════════════════════
@admin_bp.route('/messages')
@login_required
def messages():
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=msgs)


@admin_bp.route('/messages/read/<int:id>', methods=['POST'])
@login_required
def message_read(id):
    msg = ContactMessage.query.get_or_404(id)
    msg.is_read = True
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/messages/delete/<int:id>', methods=['POST'])
@login_required
def message_delete(id):
    msg = ContactMessage.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Pesan berhasil dihapus.', 'success')
    return redirect(url_for('admin.messages'))