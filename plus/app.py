from flask import Flask
import routes

app = Flask(__name__)
app.register_blueprint(routes.bp)

