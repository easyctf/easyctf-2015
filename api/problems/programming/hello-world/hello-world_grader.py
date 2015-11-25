def grade(tid, answer):
	if answer.find("welc0me_two_easyCtf") != -1:
		return { "correct": True, "message": "Great! Now you've just unlocked some more problems." }
		# return { "correct": True, "message": "Great! Now you've just unlocked some more problems." }
	return { "correct": False, "message": "If you're confused, read some tutorials :)" }