def grade(tid, answer):
	if answer.lower().find("baconont") != -1:
		return { "correct": True, "message": "It's a cool song. If you disagree I'm docking 6000 ponts >:)" }
	return { "correct": False, "message": "Man, this article is so long . . ." }