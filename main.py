import argparse
import base64
import random
import sys
import os
import json
import requests
import config


def getGithubUserDetails(username):

    try:
        head = {'Authorization': 'token {}'.format(config.GITHUB_TOKEN)}
        user_data = requests.get('https://api.github.com/users/'+username, headers=head).json()
        if "login" in user_data:
            print(username + " git user details are retrieved successfully! ", user_data)
        else:
            print(username + " git user does not exist.")
    except requests.exceptions:
        print('Bad git request')

    return user_data


# I have created the getContact function to purely call from externally to check
# if a contact id exist in the freshdesk contacts or not. This function has not been
# called anywhere in the logic as we don't have the contact id to pass
def getContact(contact_id, subdomain):

    try:
        contact = requests.get("https://" + subdomain + ".freshdesk.com/api/v2/contacts/" + contact_id,
                         auth=(config.FRESHDESK_TOKEN, config.FRESHDESK_PWD))
        if contact.status_code == 200:
            print("Contact details are retrieve successfully for contact id " + contact_id + ". Here are the details ", contact.json())
        elif contact.status_code == 404:
            print("Contact " + contact_id + " does not exists")
        else:
            print("Failed to read contact id " + contact_id + ". Status Code : " + contact.status_code)
    except:
            print('Bad request to get a contact ' + contact_id )


def createContact(contact, subdomain):

    try:
        r = requests.post("https://" + subdomain + ".freshdesk.com/api/v2/contacts",
                          auth=(config.FRESHDESK_TOKEN, config.FRESHDESK_PWD),
                          data=json.dumps(contact), headers={"Content-Type": "application/json"})

        if r.status_code == 201:
            print("Contact created successfully, the response is  ", r.content)
            print("Location Header : " + r.headers['Location'])
        else:
            print("Failed to create contact, errors are : ", json.loads(r.content))
            print("x-request-id : " + r.headers['x-request-id'] + " and Status Code : " + str(r.status_code))
    except requests.exceptions.InvalidSchema as e:
        print('Invalid url: ', e)
    except:
        print('Bad request to create a contact')


def updateContact(contact_id, new_contact_details, subdomain):

    try:
        r = requests.put("https://" + subdomain + ".freshdesk.com/api/v2/contacts/" + str(contact_id),
                             auth=(config.FRESHDESK_TOKEN, config.FRESHDESK_PWD),
                             data=json.dumps(new_contact_details), headers={"Content-Type": "application/json"})

        if r.status_code == 200:
            print("Contact updated successfully, the response is ", r.content)
        elif r.status_code == 404:
            print("Contact id " + contact_id + " does not exists.")
        else:
            print("Failed to update contact, errors are : ", json.loads(r.content))
            print("x-request-id : " + r.headers['x-request-id'] + " and Status Code : " + str(r.status_code))
    except requests.exceptions.InvalidSchema as e:
        print('Invalid url: ', e)
    except:
        print('Bad request to update a contact')


# this function will take all the freshdesk contact info, and try to check if the contact already existed
# by the email address (as the email id is unique). If the contact exists, then get the contact id and proceed
# with updateContact to update with the fresh details, if not, create a new contact
def isContactExists(freshdeskContact, subdomain):

    try:
        contact = requests.get("https://" + subdomain + ".freshdesk.com/api/v2/contacts?email=" + freshdeskContact['email'],
                         auth=(config.FRESHDESK_TOKEN, config.FRESHDESK_PWD)).json()
        if contact:
            updateContact(contact[0]['id'], freshdeskContact, subdomain)
        else:
            createContact(freshdeskContact, subdomain)
    except:
            print('Bad request to get a contact')



def mapContactDetails(gitUserData):

    #creating a dictionary for a freshdesk contact
    freshdeskContact = {"name": None,
                        "email": None,
                        "job_title": None,
                        "address": None,
                        "phone": None,
                        "twitter_id": None}

    freshdeskContact["name"] = gitUserData['name']

    # populate the email address if exists from github, otherwise mock something from name
    if gitUserData['email']:
        freshdeskContact["email"] = gitUserData['name']
    else:
        freshdeskContact["email"] = (gitUserData['name'] + '@gmail.com').replace(' ', '').lower()

    freshdeskContact["address"] = gitUserData['location']
    freshdeskContact["twitter_id"] = gitUserData['twitter_username']

    if gitUserData['bio']:
        freshdeskContact["job_title"] = gitUserData['bio']

    # mocking up a phone number
    freshdeskContact["phone"] = str(random.randint(100,999)) + '-' + \
                                str(random.randint(0,999)).zfill(3) + '-' + \
                                str(random.randint(0,9999)).zfill(4)

    return freshdeskContact


def main(gituser, subdomain):

    # retrieve the github user information
    gitUserData = getGithubUserDetails(gituser)

    #map the github information as per the freshdesh contact fields
    freshdeskContact = mapContactDetails(gitUserData)

    #check if the contact already exists in freshdesk,
    #if yes, update the contact, else create a new one
    isContactExists(freshdeskContact, subdomain)


if __name__ == '__main__':
    app_nm = os.path.basename(__file__)
    parser = argparse.ArgumentParser(description=app_nm)

    # paramaters passed to this modul
    # 1. --gituser = Github username
    # 2. --subdomain =  Freshdesk subdomain
    parser.add_argument('--gituser', action='store', dest='gituser', type=str)
    parser.add_argument('--subdomain', action='store', dest='subdomain', type=str)
    args = parser.parse_args()

    main(args.gituser, args.subdomain)
    sys.exit(0)




