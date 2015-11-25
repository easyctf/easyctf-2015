def grade(tid, answer):
	if answer.find("file_get_contents_is_9_safe") != -1:
		return { "correct": True, "message": "That's right! Maybe I should have protected it better..." }
	return { "correct": False, "message": "Nope, try again!" }