def grade(tid, answer):
	if answer.lower().find("505050") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "Nope, try again!" }