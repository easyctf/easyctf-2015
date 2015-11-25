def grade(tid, answer):
	if answer.find("at_least_im_better_than_caesar") != -1:
		return { "correct": True, "message": "Good job!" }
	return { "correct": False, "message": "Nope. Try again." }