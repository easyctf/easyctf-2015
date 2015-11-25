def grade(tid, answer):
	if answer.find("is_it_hi_or_hey_or_something_else") != -1:
		return { "correct": True, "message": "Great! Now you've just unlocked some more programming problems." }
	return { "correct": False, "message": "If you're confused, read some tutorials :)" }