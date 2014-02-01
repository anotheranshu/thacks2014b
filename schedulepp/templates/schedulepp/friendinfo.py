import facebook
import json

#Given a user's access token, generates a JSON file of their friends
def makeFriends(accessToken):
    oauth_access_token = "CAAC101zVZAO0BAKjkwJf7D5zgQUmplVAKHcCzE06Rd7UL8WKuuDmJdq17aeSZBkUL7wFFYZBEnJrSUOoJuYut9sSFcIcfKf1SU2NjBhURyjfFmMZBn3zKEtTlB9I5ZAc1VA5BSHWXmoWNdDuMH8vi81aAdNX1anBqqm9OTrPJqnPlAhJlMmEAQeRSMaXnsBKZBiVG8kTeSrgZDZD"
    graph = facebook.GraphAPI(oauth_access_token)
    friends = graph.get_connections("me", "friends")
    friendslist = friends['data']
    result = json.dumps(friendslist)
    return result



