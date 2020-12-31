#! python3.9
#python3 graphing_whatsapp_messages.py



#load file
#split into lines
#get date, time, person

#Comparables - number of texts per person, average length of text, first to initiate each day, time to respond to each message


import re
import os
from datetime import datetime, timedelta

class Sender:
		def __init__(self):
			self.name = ''
			self.number_of_messages = 0
			self.average_time_to_respond = timedelta
			self.average_words_per_message = 0

class Message:
		def __init__(self,date_time):
			self.date_time = date_time
			self.sender = Sender()
			self.contents = 'No Contents'
			self.time_to_respond = timedelta #won't need this eventually


def get_message_string_list_from(file_at_complete_path): #if the file exists, it just adds to the end
	message_string_list = []
	date_time_regex = '(?<=\[).+?(?=\])'

	realFile = open(file_at_complete_path, 'r')  
	line_list = realFile.readlines()
	realFile.close() 

	for line in line_list:
		match = re.search(date_time_regex,line)
		if match:
			message_string_list.append(line)
	return message_string_list #doesn't exclude non date prefixed lines

def get_message_attributes_from(message_string_list, unique_sender_object_list):
	date_time_regex = '(?<=\[).+?(?=\])'    #'(?<=\[).+?(?=\])'
	sender_name_regex = '(?<=\] ).+?(?=\:)'    #'(?<=\]).+?(?=\:)'
	contents_regex = '(?<=\: ).+?(?=\n)'

	date_time_as_string = re.search(date_time_regex, message_string_list).group(0).replace(',', '')
	datetime_object = datetime.strptime(date_time_as_string, '%Y-%m-%d %I:%M:%S %p')
	sender_name = re.search(sender_name_regex, message_string_list).group(0)

	
	this_message_object = Message(datetime_object)
	this_message_object.contents = re.search(contents_regex, message_string_list).group(0)
	for unique_sender_object in unique_sender_object_list:
		if sender_name == unique_sender_object.name:
			this_message_object.sender = unique_sender_object

	return this_message_object

def get_unique_sender_object_list_from(message_string_list):  #this doesn't work
	all_sender_names_list = []
	unique_sender_object_list = []
	sender_name_regex = '(?<=\] ).+?(?=\:)'    #'(?<=\]).+?(?=\:)'
	for message_string in message_string_list:
		sender_name = re.search(sender_name_regex, message_string).group(0)
		all_sender_names_list.append(sender_name)
	#remove duplicates
	unique_sender_names_list = list(set(all_sender_names_list))
	for unique_sender_name in unique_sender_names_list:
		this_sender = Sender()
		this_sender.name = unique_sender_name
		unique_sender_object_list.append(this_sender)
		#print(this_sender.name)
	return unique_sender_object_list

def get_number_of_messages_from(message_object_list, unique_sender_object_list):
	for message_object in message_object_list:
		if message_object.sender.name == unique_sender_object_list[0].name:
			message_object.sender.number_of_messages += 1
		elif message_object.sender.name == unique_sender_object_list[1].name:
			message_object.sender.number_of_messages += 1
			
	# print(f'{unique_sender_object_list[0].name}: {unique_sender_object_list[0].number_of_messages}')
	# print(f'{unique_sender_object_list[1].name}: {unique_sender_object_list[1].number_of_messages}')

def get_word_count_from(message_object_list, unique_sender_object_list):
	first_word_count_list = []
	second_word_count_list = []
	
	for message_object in message_object_list:
		if message_object.sender.name == unique_sender_object_list[0].name:
			number_of_words_in_message = len(message_object.contents.split())
			first_word_count_list.append(number_of_words_in_message)
		elif message_object.sender.name == unique_sender_object_list[1].name:
			number_of_words_in_message = len(message_object.contents.split())
			second_word_count_list.append(number_of_words_in_message)
	unique_sender_object_list[0].average_words_per_message = round(sum(first_word_count_list) / len(first_word_count_list))		
	unique_sender_object_list[1].average_words_per_message = round(sum(second_word_count_list) / len(second_word_count_list))

			
	# print(f'{unique_sender_object_list[0].name}: Average number of words per message:{round(unique_sender_object_list[0].average_words_per_message, 0)}')
	# print(f'{unique_sender_object_list[1].name}: Average number of words per message:{round(unique_sender_object_list[1].average_words_per_message, 1)}')




def get_average_response_time_from(message_object_list, unique_sender_object_list):
	first_sender_reponse_time_list = []
	second_sender_reponse_time_list = []
	for i in range(len(message_object_list)): #for i in range 200
		if i < len(message_object_list)-1: #if i (0..199) is less than 200
			first_message =  message_object_list[i]
			second_message = message_object_list[i+1]

			if first_message.sender.name != second_message.sender.name:
				this_message_response_time = second_message.date_time - first_message.date_time #remove all responses to themselves
				if this_message_response_time < timedelta(hours = 12): #ignore responses afer 8 hrs
					if second_message.sender.name == unique_sender_object_list[0].name:
						first_sender_reponse_time_list.append(this_message_response_time)
						#print(f'{unique_sender_object_list[0].name} responded to {unique_sender_object_list[1].name} in {this_message_response_time}.')
					elif second_message.sender.name == unique_sender_object_list[1].name:
						second_sender_reponse_time_list.append(this_message_response_time)
						#print(f'{unique_sender_object_list[1].name} responded to {unique_sender_object_list[0].name} in {this_message_response_time}.')
		#will have to change this for only days
	unique_sender_object_list[0].average_time_to_respond = sum(first_sender_reponse_time_list,timedelta(0)) / len(first_sender_reponse_time_list)					
	unique_sender_object_list[1].average_time_to_respond = sum(second_sender_reponse_time_list,timedelta(0)) / len(second_sender_reponse_time_list)

#-------------------------------------------------VARIABLES-------------------------------

path = '/Users/Jamie/Desktop/my_python_projects/JF_analyzing_texts/'
file_name = '_chat.txt'


#-----------------------------------------------------BEGIN-------------------------------
message_object_list = []
#file_at_complete_path = os.path.join(path, filename)
message_string_list = get_message_string_list_from(os.path.join(path, file_name))
unique_sender_object_list = get_unique_sender_object_list_from(message_string_list)

for message_string in message_string_list:
	this_message_object = get_message_attributes_from(message_string, unique_sender_object_list)
	message_object_list.append(this_message_object)


get_number_of_messages_from(message_object_list, unique_sender_object_list)
get_word_count_from(message_object_list, unique_sender_object_list)
get_average_response_time_from(message_object_list, unique_sender_object_list)




# for message_object in message_object_list:
# 	print(message_object.date_time)
# 	print(message_object.sender.name)
# 	print(message_object.contents)
# 	print()
	
	
for unique_sender_object in unique_sender_object_list:
	print(f'Sender: {unique_sender_object.name}')
	print(f'Number of messages: {unique_sender_object.number_of_messages}')
	print(f'Average number of words per message: {unique_sender_object.average_words_per_message}')
	print(f'Average time to respond: {unique_sender_object.average_time_to_respond}')
	print()

# # Timedelta function demonstration 
# from datetime import datetime, timedelta 

# # Using current time 
# ini_time_for_now = datetime.now() 

# # printing initial_date 
# print ("initial_date", str(ini_time_for_now)) 

# # Some another datetime 
# new_final_time = ini_time_for_now + \ 
# 				timedelta(days = 2) 

# # printing new final_date 
# print ("new_final_time", str(new_final_time)) 


# # printing calculated past_dates 
# print('Time difference:', str(new_final_time - \ 
# 							ini_time_for_now)) 


# datetime_str = '09/19/18 13:55:26'

# datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %I:%M:%S:%p')

# print(type(datetime_object))
# print(datetime_object)  # printed in default format