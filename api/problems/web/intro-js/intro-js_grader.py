def grade(tid, answer):
	if answer.find("developer_console_is_your_friend") != -1:
		return { "correct": True, "message": "It only gets harder from here!" }
	return { "correct": False, "message": "Nope." }