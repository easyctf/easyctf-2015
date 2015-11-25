def grade(tid, answer):
	if answer.find("?v=8ruJBKFrRCk") != -1:
		return { "correct": True, "message": "Congrats." }
	return { "correct": False, "message": "If you're confused, read some tutorials :)" }