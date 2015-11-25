def grade(tid, answer):
	if answer.find("pcap_fun!??") != -1:
		return { "correct": True, "message": "Nice! I knew they were communicating" }
	return { "correct": False, "message": "Nope! You're looking for a specific type of file" }