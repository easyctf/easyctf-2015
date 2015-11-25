def grade(tid, answer):
	if answer.find("it's_over_9000!!!") != -1:
		return { "correct": True, "message": "Great job! :D" }
	return { "correct": False, "message": "Nope. Keep clicking!" }