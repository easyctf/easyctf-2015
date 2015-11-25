def grade(tid, answer):
	if answer.find("filtering_the_#s_out") != -1:
		return { "correct": True, "message": "Great! Now you've just unlocked some more programming problems." }
	return { "correct": False, "message": "If you're confused, read some tutorials :)" }