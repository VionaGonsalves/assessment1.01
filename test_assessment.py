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


def test_home(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/?name="Viona"')
    assert resp.status_code == 200


dict_new_student = {"name": "Donson", "class_id": "334362524032507595502370532083679504284", "class_leader": "Yes"}
dict_new_student2 = {"name": "Sean", "class_id": "59369352943334187764735699285760419740", "class_leader": "No"}

dict_new_class = {"class_name": "BE IT"}

dict_update = {"id": "3564711771943327061460740174056138652", "name": "Sydney",
               "class_id": "59369352943334187764735699285760419740",
               "class_leader": "Yes"}
dict_update2 = {"id": "12654194566113633927053509605750613916", "name": "Sydney",
                "class_id": "59369352943334187764735699285760419740", "class_leader": "No"}


dict_delete = {"id": "181059901130796733222743252984573077404"}


def test_new_student(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_student', data=dict_new_student)
    assert resp.status_code == 302


def test_new_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_class_record', data=dict_new_class)
    assert resp.status_code == 302


def test_update_rec(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update_rec', data=dict_update)
    assert resp.status_code == 200


def test_delete(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/delete_student', data=dict_delete)
    assert resp.status_code == 200


def test_update(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update')
    assert resp.status_code == 200


def test_update_rec2(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update_rec', data=dict_update2)
    assert resp.status_code == 200


def test_new_student2(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_student', data=dict_new_student)
    assert resp.status_code == 302


def test_class_table(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/class_table')
    assert resp.status_code == 200

