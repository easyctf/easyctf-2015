def grade(tid, answer):
	if answer.find("'twas_sum_EZ_programming,_am_I_rite?") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "If you're confused, read some tutorials :)" }