def grade(tid, answer):
	if answer.find("yunoo0oooooooooooo0o") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Where have I seen this picture before?" }