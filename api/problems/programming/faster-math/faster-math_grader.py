def grade(tid, answer):
	if answer.lower().find("a+_for_a+_eff0rt!") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Try again :/" }