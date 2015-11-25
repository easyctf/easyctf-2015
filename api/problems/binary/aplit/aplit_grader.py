def grade(tid, answer):
	if answer.find("essays_are_too_hard") != -1:
		return { "correct": True, "message": "Nice." }
	return { "correct": False, "message": "Nope, try again!" }