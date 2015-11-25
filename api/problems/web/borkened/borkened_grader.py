def grade(tid, answer):
	if answer.find("h4xxing_th3_c0mpetition_s1t3") != -1:
		return { "correct": True, "message": "Good job!" }
	return { "correct": False, "message": "Nope, try again!" }