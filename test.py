
import os
import unittest
import sys
import requests
# Find path to the directory above the file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from kanban import app,db,Task
TEST_DB = 'test.db'

'''
This part helps set up the app as an object, which we can later test the object.
'''

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
    
    def test_about_page(self):
        '''
        Test that the about page is loaded successfully.
        '''
        req = self.app.get('/about', follow_redirects=True)
        self.assertEqual(req.status_code, 200)
        

    def test_add(self):
        '''
        Test that the method add is successful.
        '''        
        test_title = 'Testing'
        # Try adding the task "Testing"
        #Add a new task
        req = self.app.post('/add', data = dict(title=test_title),follow_redirects = True)
        #all tasks added would be deleted afterwards. 
        # Those two lines below do that. 
        act = Task.query.filter_by(title=test_title).first()
        self.app.get('/delete/'+str(act.id), follow_redirects=True)
        #check whether the response status is correct.
        self.assertEqual(req.status_code, 200)


    def test_update(self):
        '''
        Test that the method update is loaded successfully.
        ''' 
        #added a new task with test_title = "Update"
        test_title = 'Update'
        self.app.post('/add', 
                      data = dict(title=test_title),
                      follow_redirects = True)
        #Query the data with specified chose title
        act = Task.query.filter_by(title=test_title).first()
        #add new task
        req = self.app.get('/update/'+str(act.id)+'/Doing', data=dict(id = act.id))
         #all tasks added would be deleted afterwards. 
        # Those two lines below do that. 
        act2 = Task.query.filter_by(title=test_title).first()
        #check whether the response status for update method is correct.
        self.app.get('/delete/'+str(act2.id), follow_redirects=True)
        self.assertEqual(req.status_code, 302)

    
    def test_delete(self):  
        '''
        Test that the method delete is loaded successfully.
        '''   
        test_title = 'Delete'
        #added a new task with test_title = "Delete"
        self.app.post('/add', 
                      data = dict(title=test_title),
                      follow_redirects = True)
        #Query the data with specified chose title
        act = Task.query.filter_by(title=test_title).first()
        #delete the task
        req = self.app.get('/delete/'+str(act.id), follow_redirects=True)
        #check whether the response status for delete method is correct
        self.assertEqual(req.status_code, 200)

    def test_combination(self):
        '''
        Test three methods at the same time
        '''
        test_title = 'Combo'
        #added a new task with test_title = "Combo"
        #Add new task
        req1 = self.app.post('/add', 
                      data = dict(title=test_title),
                      follow_redirects = True)
        #Check whether the response for add method is correct
        self.assertEqual(req1.status_code, 200)
        act = Task.query.filter_by(title=test_title).first()
        #Update new task
        req2 = self.app.get('/update/'+str(act.id)+'/Doing', data=dict(id = act.id))
        #Check whether the response for update method is correct
        self.assertEqual(req2.status_code, 302)
        act2 = Task.query.filter_by(title=test_title).first()
        #Delete the task
        req3 = self.app.get('/delete/'+str(act2.id), follow_redirects=True)
        #Check the response status is as expected.
        self.assertEqual(req3.status_code, 200)



if __name__ == "__main__":
     unittest.main()