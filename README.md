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

Please use [OpenCTF](https://github.com/EasyCTF/OpenCTF). This repository will be left up for historical purposes.  

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
