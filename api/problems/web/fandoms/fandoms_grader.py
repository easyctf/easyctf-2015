def grade(tid, answer):
	if answer.find("geico_geck0s") != -1:
		return { "correct": True, "message": "Nice!" }
	return { "correct": False, "message": "Try again!" }