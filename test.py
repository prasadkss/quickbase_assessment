import unittest
import main


class TestContact(unittest.TestCase):

    def test_updatecontact(self):
        main.updateContact('73020866863',{"name": "test name 1", "email": "testname1012@gmail.com"}, 'kintali')

    def test_createcontact(self):
        main.createContact({"name": "test name 1", "email": "testname101@gmail.com"}, 'kintali') #73020809491
        main.createContact({"name": "test name 6", "email": "testname22@gmail.com"}, 'kintali') #73020809492

    def test_getcontact(self):
        main.getContact('73020866863', 'kintali')
        main.getContact('73024567457', 'kintali')
        main.getContact('73020809491', 'kintali')

    def test_gituser(self):
        main.getGithubUserDetails('di')
        main.getGithubUserDetails('mojombo')
        main.getGithubUserDetails('prasadkss')
        main.getGithubUserDetails('prasaaadkss')
        main.getGithubUserDetails('topfunky')
        main.getGithubUserDetails('railsjitsu')

if __name__ == '__main__':
    unittest.main()