# flask with dash

from flask import Flask 

def init_app():
  # TODO add config
  app = Flask(__name__)

  with app.app_context():
    import routes
    
    from dasher.dasher import init_dashapp
    app = init_dashapp(app)
    return app

if __name__ == '__main__':
  app = init_app()
  app.run()