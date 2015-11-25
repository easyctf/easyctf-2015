def grade(tid, answer):
	if answer.find("UgeVjTlmZjNFvULk") != -1:
		return { "correct": False, "message": "Great, now that you've found the file, read its contents!" }
	elif answer.find("it_must_be_pretty_hard_reading_this") != -1:
		return { "correct": True, "message": "Nice." }
	return { "correct": False, "message": "Nope, try again!" }