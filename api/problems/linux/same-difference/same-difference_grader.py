def grade(tid, answer):
	if answer.find("60a57b3974029aa012e66b05f122748b") != -1:
		return { "correct": True, "message": "Correct! So that's what they were hiding..." }
	return { "correct": False, "message": "Nope, try again!" }