def grade(tid, answer):
	if answer.find("3494") != -1:
		return { "correct": True, "message": "Good work!" }
	return { "correct": False, "message": "If you're confused, use Google! :)" }