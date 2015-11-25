def grade(tid, answer):
	if answer.find("failed_up_is_the_best_fail_you_are_ctf_champion") != -1:
		return { "correct": False, "message": "It's not going to be the same as last year's...." }
	if answer.find("yeee3ee3ew_sha44aal11l1l1l_bE#eeee_azzzzzsimmileitted!!") != -1:
		return { "correct": True, "message": "Now send the writeup to <code>failed.down@gmail.com</code>" }
	return { "correct": False, "message": "Keep... looking........ harder............." }