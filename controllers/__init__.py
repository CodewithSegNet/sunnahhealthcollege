#!/usr/bin/env python3

from .grade_controller import StudentScoreForm
from .pageroute import pages_bp
from .models_controller import user_bp
from views.pageViews import * 

def register_blueprints(app):
    app.register_blueprint(pages_bp)
    app.register_blueprint(user_bp, url_prefix='/api')
