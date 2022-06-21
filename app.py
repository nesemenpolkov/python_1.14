from flask import Flask, render_template
from controllers.event_controller import events


app = Flask(__name__)
app.register_blueprint(events)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run("127.0.0.1", 8001)
