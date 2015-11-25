def grade(tid, answer):
	if answer.find("can't_touch_the_ceiling") != -1:
		return { "correct": True, "message": "Good job." }
	return { "correct": False, "message": "Nope. Try again." }