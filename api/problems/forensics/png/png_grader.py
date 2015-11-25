def grade(tid, answer):
	if answer.find("troll3d") != -1:
		return { "correct": True, "message": "See! I told you something was missing" }
	return { "correct": False, "message": "Someone is hiding something . . ."}