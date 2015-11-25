def grade(tid, answer):
	if answer.find("never_trust_se1f_signd_certificates") != -1:
		return { "correct": True, "message": "Nice!" }
	return { "correct": False, "message": "Nope, try again!" }