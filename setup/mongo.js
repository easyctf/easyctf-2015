print("Setting indexes");
print("----------------------");

db.createCollection("users");
db.createCollection("teams");
db.createCollection("problems");
db.createCollection("submissions");
db.createCollection("shell_accounts");
db.createCollection("programs");
db.createCollection("password_reset");

db.submissions.ensureIndex({ "pid": 1, "tid": 1, "correct": 1, "answer": 1 }, { unique: true });
db.submissions.ensureIndex({ "tid": 1 });
db.submissions.ensureIndex({ "pid": 1 });

db.problems.ensureIndex({ "title": 1 }, { unique: true });
db.problems.ensureIndex({ "pid": 1, }, { unique: true });

db.teams.ensureIndex({ "tid": 1 }, { unique: true });
db.teams.ensureIndex({ "name": 1 }, { unique: true });

db.users.ensureIndex({ "username": 1 }, { unique: true });

print("");
