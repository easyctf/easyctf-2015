def grade(tid, answer):
	if answer.find("c0mp1et3ly_r3kt") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Nope, try again!" }