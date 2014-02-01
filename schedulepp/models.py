from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json
import re

#########################################################
  # Student Class                                       #
#########################################################

# refer to https://docs.djangoproject.com/en/dev/topics/db/managers
# section Calling custom QuerySet methods from Manager 
class StudentManager(models.Manager):

  ####################################
  # Query Database Methods           #
  ####################################

  # check if user is free in stime-etime slot, returns boolean value
  def is_free(self, self_stime, self_etime):
    schedule = self.get_schedule()
    free = True
    self_day = self_stime[0] # assuming stime/etime have same days
    self_stime = int(self_stime[1:])
    self_etime = int(self_etime[1:])
    # iterate through all classes
    for class_item in schedule: 
      class_time = class_item['time']
      # iterate through time items 
      for time in class_time: 
        # iterate through days, find matching day times 
        days = re.findall('[A-Z]+', time)[0]
        for day in days: 
            if (day == self_day): 
                # matching day, extract stime/etime
                times = re.sub('[A-Z]+', '', time).split(':')
                stime = int(times[0])
                etime = int(times[1])
                # check if stime/etime not conflicting with self stime/etime
                if (not ((self_etime < stime) or (self_stime > etime))): 
                    # conflicting times
                    return False
    # iterate through all commitments
    #commitments = self.get_commitments()
    #iterate through all commitments
    #for commitment in commitments: 
    #  commitment_day = commitment[0] # assuming stime/etime have same days
    #  commitment_time = re.sub('[A-Z]+', '', commitment).split(':')
    #  commitment_day_stime = int(commitment_time[0])
    #  commitment_day_etime = int(commitment_time[1])
    #  if (commitment_day == self_day): 
        # matching day, extract stime/etime
    #    times = re.sub('[A-Z]+', '', time).split(':')
    #   stime = int(times[0])
    #    etime = int(times[1])
        # check if stime/etime not conflicting with self stime/etime
    #    if (not ((self_etime < stime) or (self_stime > etime))): 
          # conflicting times
    #      return False

    return True

    # check if the user has mutual classes with another user, 
    # returns no. mutual classes
    def num_mutual_class(self1, self2): 
      schedule1 = self1.get_schedule()
      schedule2 = self2.get_schedule()
      classes1 = set()
      classes2 = set()
      student_obj = {}
      student_obj['name'] = self1['user']
      # iterate through all classes of user1, add classes to set
      for class_item in schedule1: 
        class_name = schedule1['class_name']
        classes1.add(class_name)
      # iterate through all classes of user2, add classes to set
      for class_item in schedule2: 
        class_name = schedule2['class_name']
        classes2.add(class_name)
      # find mutual classes 
      classes_mutual = classes1.intersection(classes2)
      student_obj['mutual_classes'] = len(classes_mutual)
      return student_obj

    # get the number of mutual friends the user has with another user
    # returns no. mutual friends
    def num_mutual_friends(self1, self2): 
      friend_list1 = self1.get_friend_list()
      friend_list2 = self2.get_friend_list()
      friends1 = set()
      friends2 = set()
      student_obj = {}
      student_obj['name'] = self1['user']
      # iterate through all classes of user1, add classes to set
      for friend in friends1: 
        friends1.add(friend)
      # iterate through all classes of user2, add classes to set
      for friend in friends2: 
        friends2.add(friend)
      # find mutual classes 
      friends_mutual = friends1.intersection(friends2)
      student_obj['num_mutual_friends'] = len(set_mutual)
      return student_obj

    # get the number of mutual friends the user has with another user
    # returns no. mutual friends
    def mutual_friends(self1, self2): 
      friend_list1 = self1.get_friend_list()
      friend_list2 = self2.get_friend_list()
      friends1 = set()
      friends2 = set()
      student_obj = {}
      student_obj['name'] = self1['user']
      # iterate through all classes of user1, add classes to set
      for friend in friends1: 
        friends1.add(friend)
      # iterate through all classes of user2, add classes to set
      for friend in friends2: 
        friends2.add(friend)
      # find mutual classes 
      friends_mutual = friends1.intersection(friends2)
      student_obj['mutual_friends'] = list(friends_mutual)
      return student_obj

  def get_queryset(self): 
    return super(StudentManager, self).get_queryset()

  # returns set of students who are free in a given time interval
  def are_free(stime, etime): 
    students = get_queryset() 
    free_students = []
    for student in students: 
      if (is_free(student, stime, etime)): 
        free_students.append(student)
    return free_students

  # get the mutual classes of a student with other students
  def mutual_classes(self): 
    students = get_queryset()
    mutual_classes_list = []
    for student in students: 
      mutual_classes_list.append(students.num_mutual_classes(self, student))
    return mutual_classes_list

  # get the mutual friends of a student other students
  def num_mutual_friends(self):
    students = get_queryset()
    mutual_friends_list = []
    for student in students: 
      mutual_students_list.append(students.mutual_students(self, student))
    return mutual_students_list

  ####################################
  # Create methods                   #
  ####################################

  # create student object
  def create_student(self, fb_id, first_name, last_name, friends):
  # create student object
  	student = self.create(fb_id=fb_id, first_name=first_name, last_name=last_name, 
                        friend_list=friend_list)
  	student.save()
  	return student

#########################################################
  # Student Class                                       #
#########################################################

class Student(models.Model):
  fb_id = models.IntegerField(default=0, primary_key=True)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  schedule = models.CharField(max_length=5000) 
  friend_list = models.CharField(max_length=5000)
  #preferences = models.CharField(max_length=5000) # rank preferences (lunch, workout, study group)
  #commitments = models.CharField(max_length=5000) # list of time commitments (time slots)
  # andrew = models.CharField(max_length=100)
  objects = StudentManager()

  ################################
  # Getter Methods 
  #(returns native format objects)
  ################################

  # get the user schedule 
  def get_schedule(self): 
    schedule = json.loads(self.schedule)
    return schedule

  # get all the friends a student
  def get_friend_list(self): 
    friend_list = json.loads(self.friend_list)
    return friend_list

  # get all the preferences of a student
  # Format: {activity: "ACTIVITY", rating: "SCORE (0-3), 
  #preference decreases with increasing value"}
  #def get_preferences(self): 
  #  preferences = json.loads(self.preferences)
  #  return preferences

  # get all the extra time commitments of a student
  # Format: array of string representing days/time
  #def get_commitments(self): 
  #  return self.commitments

  ################################
  # Update Methods 
  #(takes native object) 
  ################################

  # updates schedule for a student
  def update_schedule(self, schedule): 
    self.schedule = str(schedule)
    self.save()

  # updates friend list 
  def update_friend_list(self, friend_list): 
    self.friend_list = friend_list
    self.save()

  # update preferences for a student
  #def update_preferences(self, preferences): 
  #  self.preferences = preferences
  #p  self.save()

  # update commitments for a student (read in new value set)
  #def update_preferences(self, commitments): 
  #  self.commitments = commitments
  #  self.save()

#########################################################
  # Event Class Manager                                 #
#########################################################

class EventManager(models.Manager):
  # create student object
  def create_event(self, students, event_type, stime, etime): 
    num_students = len(students.split(' '))
    accepts = "pending" * num_students
    ratings = "0" * num_students

    event = self.create(students=students, event_type=event_type, 
                        stime=stime, etime=etime, accepts=accepts, 
                        ratings=ratings)
    event.save()
    return event

  ################################
  # Getter Methods 
  #(returns native format objects)
  ################################

  def get_ratings(self): 
    ratings = self.ratings.split(' ')
    return map(lambda x: int(x), ratings)

  def get_accepts(self): 
    accepts = self.accepts.split(' ')
    return accepts

  ################################
  # Update Methods 
  #(takes native object) 
  ################################

  # update accept for a given student
  def update_accepts(self, student, accept): 
    students = self.students.split(' ')
    accepts = self.accepts.split(' ')
    idx = students.index(student)
    accepts[idx] = accept
    self.accepts = accepts
    self.save()

  # update rating for a given student
  def update_ratings(self, student, rating): 
    students = self.students.split(' ')
    ratings = self.ratings.split(' ')
    idx = students.index(student)
    ratings[idx] = rating
    self.ratings = ratings
    self.save()

#########################################################
  # Event Class                                         #
#########################################################

class Event(models.Model):
  students = models.CharField(max_length=1000) # invited students
  event_type = models.CharField(max_length=100)
  stime = models.DateTimeField()
  etime = models.DateTimeField()
  accepts = models.CharField(max_length=1000) # pending/accept/decline
  ratings = models.CharField(max_length=1000) # 1-5 scale
  objects = StudentManager()
