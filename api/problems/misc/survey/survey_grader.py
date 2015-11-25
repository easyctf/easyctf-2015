def grade(tid, answer):
	if answer.find("it's_fin4lly_over!!") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "Nope, try again!" }