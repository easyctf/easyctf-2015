def grade(tid, answer):
	if answer.find("missionsuccess") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "Nope, try again!" }