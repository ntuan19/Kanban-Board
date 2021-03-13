import os
import unittest
import sys
import requests
# Find path to the directory above the file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from kanban import app,db,Task
TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):
    '''
    Execute prior to each test.
    '''
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()

    '''
    Execute after each test
    '''
    def tearDown(self):
        pass

# Tests

    def test_main_page(self):
        '''
        Test that the main page is loaded successfully.
        '''
        req = self.app.get('/', follow_redirects=True)
        self.assertEqual(req.status_code, 200)
        print("Hello the World")


    def test_add(self):        
        test_title = 'TeStIng'
        # Try adding the task "Testing"
        req = self.app.post('/add', 
                      data = dict(title=test_title),
                      follow_redirects = True)
        self.assertEqual(req.status_code, 200)
        act = Task.query.filter_by(title=test_title).first()
        self.app.get('/delete/'+str(act.id), follow_redirects=True)
        # test_title = 'TeStIng'

    def test_update(self):
        test_title = 'Update'
        # Try adding the task "Testing"
        self.app.post('/add', 
                      data = dict(title=test_title),
                      follow_redirects = True)
        act = Task.query.filter_by(title=test_title).first()
        req = self.app.get('/update/'+str(act.id)+'/Doing', data=dict(id = act.id))
        self.assertEqual(req.status_code, 302)
        act = Task.query.filter_by(title=test_title).first()
        self.app.get('/delete/'+str(act.id), follow_redirects=True)
    
    def test_delete(self):    
        test_title = 'Delete'
        # Try adding the task "Testing"
        self.app.post('/add', 
                      data = dict(title=test_title),
                      follow_redirects = True)
        act = Task.query.filter_by(title=test_title).first()
        req = self.app.get('/delete/'+str(act.id), follow_redirects=True)
        self.assertEqual(req.status_code, 200)
if __name__ == "__main__":
     unittest.main()