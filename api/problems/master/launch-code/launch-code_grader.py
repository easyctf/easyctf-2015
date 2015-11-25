def grade(tid, answer):
	if answer.lower().find("6672-50f3-c62b-7231") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "Nope, try again!" }