def grade(tid, answer):
	if answer.find("th0se_pesky_capit4ls_were_a_pa1n,_weren't_they?") != -1:
		return { "correct": True, "message": "Awesome." }
	return { "correct": False, "message": "Dang it. That's not right." }