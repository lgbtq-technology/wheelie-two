def register_blueprints(app):
    from app.routes.button import button_bp
    from app.routes.command import command_bp
    from app.routes.event import event_bp
    from app.routes.install import install_bp
    from app.routes.oauth import oauth_bp
    from app.routes.signup import signup_bp

    app.register_blueprint(install_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(command_bp)
    app.register_blueprint(button_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(signup_bp)
