def grade(tid, answer):
	if answer.find("54771309-67e5-4704-8743-6981a40b") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "Nope, that's not quite right." }