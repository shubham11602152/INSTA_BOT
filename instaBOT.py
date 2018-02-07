import requests
import urllib

APP_ACCESS_TOKEN = '4870715640.a48e759.874aba351e5147eca8a9d36b9688f494'
BASE_URL = 'https://api.instagram.com/v1/'

def self_info():


    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()


    if user_info['meta']['code'] == 200:

        if 'data' in user_info:

            print 'Username is : %s' % (user_info['data']['username'])
            print 'Full name of %s is : %s ' % (user_info['data']['username'],user_info['data']['full_name'])
            print 'No. of followers of %s : %s' % (user_info['data']['username'],user_info['data']['counts']['followed_by'])
            print 'No. of people %s are following : %s' % (user_info['data']['username'],user_info['data']['counts']['follows'])
            print 'No. of posts of %s : %s' % (user_info['data']['username'],user_info['data']['counts']['media'])

        else:

            print 'User does not exist!'

    else:

        print 'Status code other than 200 received!'


'''
Function declaration to get the ID of a user by username
'''


def get_user_id(insta_username):

    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Function declaration to get the info of a user by username
'''


def get_user_info(insta_username):

    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if 'data' in user_info:
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get your recent post
'''


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def start_bot():

    print 'Hey! Welcome to instaBot!'
    print 'Here are your menu options:'
    print " 1.Get your own details\n 2.Get details of a user by username\n 3.Get your own recent post\n 4.Get the recent post of a user by username\n 5.Exit"

    while True:

        choice = input("Enter you choice: ")
        if choice == 1:
            self_info()
        elif choice == 2:
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == 3:
            get_own_post()
        elif choice == 4:
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == 5:
            exit()
        else:
            print "wrong choice"

start_bot()
