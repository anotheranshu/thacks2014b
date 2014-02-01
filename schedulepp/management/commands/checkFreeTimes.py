from django.core.management.base import NoArgsCommand

from models import Student
import datetime

dayDict = {0: "M", 1: "T", 2: "W", 3: "R", 4: "F"}

class Command(NoArgsCommand):
	help = 'Checks if any reminders need to be sent'

	def handle_noargs(self, **options):
		time = datetime.datetime.time(datetime.datetime.now())
		day = datetime.datetime.weekday()
		suggestedEvents = []
		if (day == 5 or day == 6): # not handling Sat/Sun
			return None
		day = dayDict[day]
		# start time
		stime_str = str(time.hour()) + str(time.minute())
		# end time (one hour interval)
		etime_str = str(time.hour + 1) + str(time.minute())
		# concat day of the week
		stime_str = day + stime_str
		etime_str = day + etime_str
		# iterate over all students in database
		for student in Student.objects.all(): 
			suggestedEvents.append(student.suggestEvent(stime_str, etime_str))

			