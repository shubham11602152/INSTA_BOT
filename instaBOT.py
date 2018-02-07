import requests

APP_ACCESS_TOKEN = '4870715640.a48e759.874aba351e5147eca8a9d36b9688f494'
BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        print("Successful")
        
        print user_info['data']['username'] + " is username of instagram user"
        print user_info['data']['full_name'] + " is full name of user"
        print "Total posts %s " % user_info['data']['counts']['media']
        print "Following %s " % user_info['data']['counts']['follows']
        print "Followed by %s " % user_info['data']['counts']['followed_by']
    else:
        print 'Status code other than 200 received!'
self_info()
