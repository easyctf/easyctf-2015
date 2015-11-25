def grade(tid, answer):
	if answer.find("cr4zy_p4ssw0rds") != -1:
		return { "correct": True, "message": "Maybe sticking everything in the HTML source wasn't exactly the best idea." }
	return { "correct": False, "message": "Nope, that's not quite right." }