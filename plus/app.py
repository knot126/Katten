from flask import Flask
import routes
import flags

app = Flask(__name__)
app.register_blueprint(routes.bp)
app.register_blueprint(flags.bp)
