def grade(tid, answer):
	if answer.find("anomalously_hazardous_materials") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Nope." }