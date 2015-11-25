EasyCTF 2015
======

Introduction
------

Based on PicoCTF platform.

This is the backbone to the EasyCTF 2015 website. After the competition ends, this repository will be publicly released and donated to the public for future CTF competitions.

The EasyCTF 2015 website was developed and is run on Ubuntu 14.04 LTS; if you are using another operating system, please make the necessary adjustments to the installation instructions to adapt to your system. More specific instructions on how to run and use this website are provided below.

I removed the important keys and secrets, and tried to generalize some parts of the initial installation, but we're working on an actual CTF-in-a-box platform over at [OpenCTF](https://github.com/EasyCTF/OpenCTF). Good luck!

Installation
------

- First, obtain a server that runs Ubuntu, install git, and pull this repo to your computer.
- Note: most of the scripts and stuff should be run from the root directory of the project.
- Install all other dependencies by running the `setup/deps.sh`. Ex: `sh setup/deps.sh`
- Prepare the MongoDB database by running the `setup/mongo.js`. Ex: `mongo easyctf setup/mongo.js`
- Run `deploy` to start the server. Ex: `deploy` (you'll probably want to `. /etc/profile` to have the directory added to your path)
- If you are using a VPS, verify that port 443 (HTTPS) is open. The site should be working now.

Loading Problems
------

- Create your problems inside `/api/problems`. Make sure the directory format is `category/problem_name`
- Inside the `category/problem_name` directory, add `problem_name.json`
- In the same folder, create your grader script. To get the right path, follow the example
- In the same folder, use a `static` folder to contain static files
- Once you're done putting your problems there, run `api/load_problems.py` to copy the problems to the db

Problem-Writing Guidelines
------

- The `pid` field should be unique to every problem
- Try to maintain similar `category`s throughout the competition. For example, don't have `Misc` and `Miscellaneous`
- Threshold + weightmap are for unlocking problems. For example, if you want problem D to be unlocked after 2 of problems A, B, or C are solved, then, in problem D's `problem.json`, use weightmap `{ "A": 1, "B": 1, "C": 1 }` and threshold `2`.
- The `bonus_points` field is to award bonus points for first solvers. However, since some problems deserve a higher bonus than others, this field allows you to customize that. Even though we disabled this in EasyCTF, the feature is still there.

Contact
------

- If you need help with setting up and running this website, file an issue, or email me at failed.down@gmail.com
- This software is licensed under the MIT License. See LICENSE for details.
