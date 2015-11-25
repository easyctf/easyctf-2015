def grade(tid, answer):
	if answer.find("c0N+1nU3d_fr4c+10n5_pH1") != -1:
		return { "correct": True, "message": "Nice job! Kudos from the cat :3" }
	return { "correct": False, "message": "Nope. Try again." }