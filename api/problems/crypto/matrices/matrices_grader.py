def grade(tid, answer):
	if answer.find("4b5+r4C+10N") != -1:
		return { "correct": True, "message": "Good job!" }
	return { "correct": False, "message": "Nope. Try again." }