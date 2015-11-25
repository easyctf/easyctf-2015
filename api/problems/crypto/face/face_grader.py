def grade(tid, answer):
	if answer.find("yeymastery") != -1:
		return { "correct": True, "message": "Good job! dayvette = david x yvette (i'm such a good friend)" }
	return { "correct": False, "message": "dayvette = otp <3" }