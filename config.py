import Flask
from tempfile import mkdtemp
from flask_session import Session

app = Flask(__name__)
app.secret_key = "brendan"
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)