def grade(tid, answer):
	if answer.find("changing_things_up_once_in_a_while_is_gooood_for_you") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "If you're confused, read some tutorials :)" }