# **+@ TO PERFORM INTERNET OPERATIONS @+**
import requests


# **+@ TO DOWNLOAD MEDIA FROM INTERNET @+**
import urllib

# **+@ To IMPLEMENT nlp @+**
from textblob import TextBlob

# **+@ To IMPLEMENT TEXT ANALYSIS EITHER +VE, -VE OR NEUTRAL @+**
from textblob.sentiments import NaiveBayesAnalyzer



'''
Note: To make instabot work over your own account make a developer client account of instagram.
      Generate your own access token and use it. 
'''


'''
Note: To use any username based operation of instabot the user must be added in your sandbox.
'''



APP_ACCESS_TOKEN = 'Add your Access Token'
BASE_URL = 'https://api.instagram.com/v1/'


#*********************** +@ MODULE TO FETCH USER'S OWN INFORMATION USING INSTAGRAM API @+ ***************************************************************************

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




#*********************** +@ MODULE TO GET ID OF A USER USING USERNAME @+ ***************************************************************************

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



#*********************** +@ MODULE TO GET THE INFO OF A USER  USING USERNAME @+ ***************************************************************************

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



#*********************** +@ MODULE TO GET USER'S OWN RECENT POST @+ ***************************************************************************

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



#*********************** +@ MODULE TO GET RECENT POST OF A USER USING USERNAME @+ ***************************************************************************

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
            return user_media['data'][0]['id']

        else:

            print 'Post does not exist!'
    else:

        print 'Status code other than 200 received!'
        return None


#*********************** +@ MODULE TO LIKE A POST USING USERNAME @+ ***************************************************************************

def like_a_post(insta_username):

	media_id = get_user_post(insta_username)

	request_url = (BASE_URL + 'media/%s/likes') % (media_id)
	payload = {"access_token": APP_ACCESS_TOKEN}
	print 'POST request url : %s' % (request_url)
	post_a_like = requests.post(request_url, payload).json()

	if post_a_like['meta']['code'] == 200:

		print 'Like was successful!'

	else:

		print 'Your like was unsuccessful. Try again!'


#*********************** +@ MODULE TO DELETE NEGATIVE COMMENTS FROM A POST USING USERNAME @+ ***************************************************************************

def delete_negative_comment(insta_username):

	media_id = get_user_post(insta_username)
	request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
	print 'GET request url : %s' % (request_url)
	comment_info = requests.get(request_url).json()

	if comment_info['meta']['code'] == 200:
		# Check if we have comments on the post
		if len(comment_info['data']) > 0:
			# And then read them one by one
			for comment in comment_info['data']:

				comment_text = comment['text']
				blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

				if blob.sentiment.p_neg > blob.sentiment.p_pos:

					comment_id = comment['id']
					delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
						media_id, comment_id, APP_ACCESS_TOKEN)
					print 'DELETE request url : %s' % (delete_url)

					delete_info = requests.delete(delete_url).json()

					if delete_info['meta']['code'] == 200:

						print 'Comment successfully deleted!'

					else:

						print 'Could not delete the comment'

		else:

			print 'No comments found'

	else:

		print 'Status code other than 200 received!'



#*********************** +@ MODULE TO GET LIST OF COMMENTS USING USERNAME @+ ***************************************************************************

def get_comment_list(insta_username):

    media_id = get_user_post(insta_username)

    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    get_comment = requests.post(request_url, payload).json()

    if get_comment['meta']['code'] == 200:

        if 'data' in get_comment:

            print 'List Of Comments Is As Follows : '
            print "Comment is : %s By %s" % (get_comment['data'][0]['text'],get_comment['data'][0]['from'][1])

        else:

            print "No Comments To Display"

    else:

        print 'Your request to display list of comments was unsuccessful. Try again!'

#get_comment_list("rajat8310")


#*********************** +@ MENU FOR INSTABOT @+ *********************************************************************************************

def start_bot():


    while True:

        print 'Hey! Welcome to instaBot!'

        print 'Here are your menu options:'

        print " 1.Get your own details. \n 2.Get details of a user by username. \n 3.Get your own recent post. \n 4.Get the recent post of a user by username. \n 5.Like recent post of a user. \n 6.Delete negative comment for a user. \n 7.To Get List Of Comments. \n 8.Exit"

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

            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)

        elif choice == 6:

            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)

        elif choice == 7:

            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)

        elif choice == 8:

            exit()

        else:

            print "Wrong Choice.... Dear User Please Look At the Menu Carefully And Choose Your Relevant Activity.. "

start_bot()
