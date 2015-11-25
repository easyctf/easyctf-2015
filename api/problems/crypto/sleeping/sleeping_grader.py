def grade(tid, answer):
	if answer.lower().find("serversarehadchaosagentgotosleep") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Nope. Try again." }