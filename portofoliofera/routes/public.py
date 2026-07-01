from flask import Blueprint, render_template
from models import HeroContent, AboutContent, Skill, Experience, Project

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    hero    = HeroContent.query.first()
    about   = AboutContent.query.first()
    hard_skills    = Skill.query.filter_by(category='hard').order_by(Skill.order).all()
    mastery_skills = Skill.query.filter_by(category='mastery').order_by(Skill.order).all()
    soft_skills    = Skill.query.filter_by(category='soft').order_by(Skill.order).all()
    tools          = Skill.query.filter_by(category='tool').order_by(Skill.order).all()
    experiences    = Experience.query.order_by(Experience.order, Experience.created_at.desc()).all()
    projects       = Project.query.order_by(Project.order, Project.created_at.desc()).all()

    return render_template('index.html',
        hero=hero,
        about=about,
        hard_skills=hard_skills,
        mastery_skills=mastery_skills,
        soft_skills=soft_skills,
        tools=tools,
        experiences=experiences,
        projects=projects
    )