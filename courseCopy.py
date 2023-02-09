'''
This script will perform a course export/import in bulk.

Example use case 1:
A large number of courses need to be copied into new shells for the next semester.

Example use case 2:
A "template course" containing standardized content needs to be copied into many courses.

How to use:
This script uses a companion CSV file called "courseCopy_list.csv"
Each row consists of two columns.
The first column will contain the SIS ID of the "source course" to copy from.
The second column will contain the SIS ID of the "destination course" to copy into.
Once the CSV file has been prepared, this script may be run.
'''


# Import the Canvas API, a helpful progress bar, and the time module required for the bar
from canvasapi import Canvas
from alive_progress import alive_bar; import time

# Authentication with Canvas is handled in a separate script called 'startSession.py'
# The script only needs to be written once, then we can simply import it in all future scripts.
# The authentication script has been written to allow the user to select from a list of institutions to connect to.
import startSession
canvas = startSession.Start()[0]	# The resulting Canvas object

# Create a blank list to hold any courses that give an error.
errorList = []

# Open the CSV file
courseList = open("courseCopy_list.csv", "r")
# Put every row of the CSV into a list called allRows
allRows = courseList.read().split("\n")
# Activate the progress bar
with alive_bar(len(allRows)) as bar:
	for row in allRows:
		# Skip the header row
		if row == allRows[0]:
			pass
		else:
			# Take each row in allRows and further split into individual cells
			cellGroup = row.split(",")
			# Try to GET the source Canvas course and declare as sourceCourse
			try:
				sourceCourse = canvas.get_course(cellGroup[0], True)
			# If it fails, print an error and add the course to our errorList
			except:
				print("Could not find the source course with SIS ID: " + str(cellGroup[0]))
				errorList.append(cellGroup[1])
				continue
			# Print the target course
			for course in cellGroup[1:]:
				print("Target course cell is " + course)
				# Skip over blanks
				if course == "":
					print("Cell is blank ('" + course + "'). Skipping.")
				else:
					# Try to GET the target Canvas course and declare as targetCourse
					try:
						targetCourse = canvas.get_course(course, True)
					# If it fails, print an error and add the course to our errorList
					except:
						print("Could not find the target course with SIS ID: " + str(course))
						errorList.append(cellGroup[1])
						continue
					try:
						# THIS IS WHERE THE EXPORT/IMPORT HAPPENS
						# Create a content migration using the source and destination courses
						print("Transferring content from '" + sourceCourse.name + "' to '" + targetCourse.name + "'.")
						targetCourse.create_content_migration(
							'course_copy_importer',
							settings={
								'source_course_id': sourceCourse.id
							}
						)
						print("Content has been transferred.")
					except:
						# If it fails, print an error and add the course to our errorList	
						print("There was an error while copying courses.")
						errorList.append(cellGroup[1])
					finally:
						# Move the progress bar once the course has been copied or failed
						bar()

# The job is done!
# List any courses that gave an error so an admin can troubleshoot
print("DESTINATION courses that encountered errors while copying:")
for e in errorList:
	print(e)
