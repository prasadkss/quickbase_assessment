### **Assessment Requirements:**

Create command line Python program, which retrieves the information of a GitHub User and creates a new Contact or updates an existing contact in Freshdesk, using their respective APIs.

### **Explanation:**

Parameters needed by main.py modules 
1. --gituser = Github username
2. --subdomain =  Freshdesk subdomain

Function's in the main.py module:
1. getGithubUserDetails
2. getContact
3. createContact
4. updateContact

I have used argparse to receive them and parse the parameters into 2 fields. Once I got the user name (which is github user), I have used getGithubUserDetails function to call github api to retrieve the user details. I have populated the success and error messages appropriately.

Upon retrieving the user details from github, I have used createContact or updateContact functions to either create or update a Freshdesk contact using their API's. I have also created function getContact to retrieve the Freshdesk contact_id information if needed.

I have created a test.py module to unit test the functionality.