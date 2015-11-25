def grade(tid, answer):
	if answer.find("sorting_is_as_easy_as_3_2_1!") != -1:
		return { "correct": True, "message": "Great! Now you've just unlocked some more programming problems." }
	return { "correct": False, "message": "If you're confused, read some tutorials :)" }