from test_autodoc import TestAutodoc
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

class TestRestlessIntegration(TestAutodoc):
    def setUp(self):
        super(TestRestlessIntegration, self).setUp()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
	db = SQLAlchemy(self.app)

        class User(db.Model):
            id = db.Column(db.Integer, primary_key=True)
	    username = db.Column(db.String(80), unique=True)
	    email = db.Column(db.String(120), unique=True)
	self.db = db
	self.user_class = User

    def test_restless_api_is_documented(self):
        manager = APIManager(self.app, flask_sqlalchemy_db=self.db)
        manager.create_api(self.user_class)

        for endpoint, function in self.app.view_functions.iteritems():
            self.app.view_functions[endpoint] = self.autodoc.doc()(function) 

        with self.app.app_context():
            doc = self.autodoc.generate()
            self.assertTrue(len(doc) == 5, len(doc))
            self.assertEqual(set(d['rule'] for d in doc), set(['/api/user', '/api/user/<instid>', '/api/user/<instid>/<relationname>', '/api/user/<instid>/<relationname>/<relationinstid>']))
	    self.assertTrue(all((d['endpoint'] == 'userapi0.userapi') for d in doc))
            self.assertEqual(doc[0]['methods'], set(['OPTIONS']))
	    self.assertTrue(all((d['methods'] == set(['HEAD', 'OPTIONS', 'GET'])) for d in doc[1:]))

