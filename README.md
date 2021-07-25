# AI Snake

Play snake manually or train him using reinforced learning. Running project with a manual mode will generate data required for training snake later using normal dense layers. Player can also specify running the game with "reinforced" option to see how snake learns on his mistakes using reinforced learning.

Using reinforced learning will show that snake learns basic behavior of not eating himself after around 60+ games, and after around 90+ games snake should start reaching higher and higher scores.

Since it is just a demo to practice reinforcement learning, few small adjustments could be applied to make snake learn faster:
* Cleaning up the data buffer from junk for the best achieved score.
* Limitation of movement to only three possibilities.
* Better adjustment of the reward and punishment rate.
