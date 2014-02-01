from django.db import models
from django.contrib.auth.models import User
from schedulepp.models import *
import datetime
import random
from django.utils import simplejson as json
from django.conf import settings
import facebook
import json
import math
from random import choice
from schedule import *

#Given a user's access token, generates a JSON file of their friends
def makeFriends(accessToken):
    oauth_access_token = "CAAC101zVZAO0BAKjkwJf7D5zgQUmplVAKHcCzE06Rd7UL8WKuuDmJdq17aeSZBkUL7wFFYZBEnJrSUOoJuYut9sSFcIcfKf1SU2NjBhURyjfFmMZBn3zKEtTlB9I5ZAc1VA5BSHWXmoWNdDuMH8vi81aAdNX1anBqqm9OTrPJqnPlAhJlMmEAQeRSMaXnsBKZBiVG8kTeSrgZDZD"
    graph = facebook.GraphAPI(oauth_access_token)
    friends = graph.get_connections("me", "friends")
    friendslist = friends['data']
    result = json.dumps(friendslist)
    return result

#gets the ID of the current user, returned as a string
def getMyId(accessToken):
    oauth_access_token = "CAAC101zVZAO0BAIaMjZC1orWTs3KQnUuY66108iLbyW0QT3oPhphejlTCCU22ZBprTNFy67DSZCTx0db6ZBX454KwEKXVa2iHZBpsIpVaCJh5mnK3yJhVLaDBqOkVWbKxYwuQ6SRk3rfNkuIPCC6K3FUkSOL5KDFMswMqZCY5m1RVPLjhNnZB0OBwR143z4CibQY6IFWzDabWwZDZD"
    graph = facebook.GraphAPI(oauth_access_token)
    me = graph.get_object("me")
    id = me["id"];

#Given the access token and the ID number of a FB user, return a JSON of the user's friends.
def findUserFriends(accessToken, idNum):
    accessToken = "CAAC101zVZAO0BAKjkwJf7D5zgQUmplVAKHcCzE06Rd7UL8WKuuDmJdq17aeSZBkUL7wFFYZBEnJrSUOoJuYut9sSFcIcfKf1SU2NjBhURyjfFmMZBn3zKEtTlB9I5ZAc1VA5BSHWXmoWNdDuMH8vi81aAdNX1anBqqm9OTrPJqnPlAhJlMmEAQeRSMaXnsBKZBiVG8kTeSrgZDZD"
    graph = facebook.GraphAPI(accessToken)
    profile = graph.get_object(str(idNum))
    friends = graph.get_connections(str(idNum), "friends")
    friendslist = friends['data']
    result = json.dumps(friendslist)
    return result

def diff(a, b):
  b = set(b)
  return [aa for aa in a if aa not in b]

def intersect(a, b):
  b = set(b)
  return [aa for aa in a if aa in b]
    
def is_user(authtok):
  if (authtok):
    graph = facebook.GraphAPI(authtok)
    if (graph):
      id_num = (graph.get_object("me"))["id"]
      print str(id_num)
      return True  #THIS LINE IS ONLY HERE FOR TESTING BEFORE WE ACTUALLY SET UP THE DATABASE
      return (len(Student.objects.filter(fb_id=int(id_num))) > 0)
  return False

def find_min_weight_friend(suggested_friends): 
  min_weight = -1
  min_weight_friend = null
  for friend_suggestion in suggested_friends: 
    if (min_weight == -1 or friend_suggestion['weight'] < min_weight): 
      min_weight = friend_suggestion['weight']
      min_weight_friend = friend_suggestion
  return min_weight_friend

def choose_top_friends(possible_friends): 
  suggested_friends = []
  max_friends = 3
  # iterate through set of possible friends
  for friend in possible_friends: 
    friend_weight = friend['weight']
    # if not reached max_friends, continue adding friends
    if (len(suggested_friends) < max_friends): 
      suggested_friends.append(friend)
    else: 
      # return min weight/min weight friend
      min_weight_friend = find_min_weight_friend(suggested_friends)
      # check if min weight less than current weight
      if (min_weight_friend['weight'] < friend_weight): 
        # remove min_weight_friend from list, add friend
        suggested_friends.remove(min_weight_friend)
        suggested_friends.add(friend)
  return suggested_friends

def suggestEvent(self, self_stime, self_etime): 
  possible_friends = []
  # check if free currently
  if (is_free(self, self_stime, self_etime)): 
    # get all people with same free timeslot
    other_free_people = are_free(self_stime, self_etime)
    # check to see which people have same classes as you
    mutual_class_people = filtered_num_mutual_friends(self, other_free_people)
    # for each person, calculate a weighted value (number common classes, 
    # number mutual friends 
    for student in other_free_people: 
      student_obj = create_student_obj(student)
      num_classes = student['num_classes']
      num_friends = student['name']
      weighted_val = num_friends + math.pow(num_classes, 3)
      student_obj['weight'] = weighted_val
      possible_friends.append(student_obj)
    suggest_friends = choose_top_friends(possible_friends)
    # choose highest weighted friends (1-3)
    suggested_friends = choose_top_friends(possible_friends)
    # return randomly choosen friend from list
    return choice(suggested_friends)
  else: 
    # not currently free
    return None

def create_user(authtok):
  if (authtok):
    graph = facebook.GraphAPI(authtok)
    if (graph):
      me = graph.get_object("me")
      friends = (graph.get_connections("me", "friends"))["data"]
      student = Student.create_student(me["id"], me["first_name"], me["last_name"], json.dumps(friends))
      return student
  return None

def update_sio(authtok, andrew, passwd):
  if (authtok): 
    graph = facebook.GraphAPI(authtok)
    if (graph):
      me = graph.get_object("me")
      fb_id = me["id"] 
      # get schedule, save to student object
      schedule = json.dumps(get_sio(andrew, passwd))
      student = Student.objects.get(fb_id=fb_id)
      student.update_schedule(schedule)
      return student
    return None
  return None




  
