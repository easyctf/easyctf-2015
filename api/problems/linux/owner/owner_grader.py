def grade(tid, answer):
	if answer.find("leonidas:sparta") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Nope, try again!" }