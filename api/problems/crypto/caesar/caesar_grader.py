def grade(tid, answer):
	if answer.find("Nap0leon_vs_Ca3s4r") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Not shifty enough!" }