import pytest
import main
import flask
from main import*
from flask.testing import FlaskClient

# Connection to the database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:viona@localhost/testcheck'
app.config['SECRET_KEY'] = "vionag"
DB = SQLAlchemy(APP)


@pytest.fixture(scope='module')
def test_resp_code():
    client = main.APP.test_client()
    return client
