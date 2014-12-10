project_alpha
=============

**Make sure to conform all code to the [Official Style Guide for Python](http://legacy.python.org/dev/peps/pep-0008/)**

=======
Do we want a couple of readme's:

• urgent issues (use issues method for this, I'm assuming)
• task assignments, updates, misc issues & questions
• ideas for consideration or later development

###---Story Ideas (feel free to add)---
Nameless person from some town 
your sheep have been killed by killer rabits that appered out of nowere.
you have to go find the monster resposible for unleashing these rabbits.
Make sure not to forget proper colon care while on your quest.

###---Working Priorities---

We need two map types. Battle Map and Overworld.

1. creating the map

2. sprite movement

3. turns

4. unite turn priority

###---ART NOTES---

800x600 screen size

12x12pixel sprite size


###---STAT INFO/IDEAS---

(Str) Pertains to physical ability, melee and to some degree ranged damage, moving objects,
could also effect Intimidation. Also effects how much/heavy of armor you can wear.

(Dex) Pertains to reflexes, movement, ability to dodge, melee/ranged damage, could also effect Kinesthetic Sense.
Also effects the ammount of armor you have due to your ability to utilize it more effectively (i.e. blocking incoming dmg with thicker parts of armor).
(Con) Pertains to
(Int) Pertains to
(Wis) Pertains to
(Chs) Pertains to
(Lck) Pertains to

###---Skill INFO/IDEAS---

These are mostly all for latter use but I wanted to get the ball rolling.

For skills I am thinking along the lines of stealing a bit from Dwarf Fortress and D&D since
they pretty much got everything right already and follow a more realistic design.

Speach
Language
Perseption
Common Sense
Kinesthetic Sense
Intuition
Intimidate
Willpower
Focus
Analytical Ability

###---Dad is working on---
combat windows:
Possible Pre-Combat Order:
• Create battle map
• Position enemy units - if in LOS, reveal
• Select unit types (if more than one type)
• Position Units
• Give units initial command series (like cards in a card game)
• Begin Turn order

Possible Turn Order:
• Verify unit is alive
• Verify unit is not stunned/stuck/disabled/hidden or timed command
• Verify unit is not in melee (if in melee and moves away, penalty or opponent attack applies)
• Move towards target area (question - how far move each turn?)
  - determine next square
  - if legal, move into square
  - verify if unit becomes engaged in melee
  - if remaining movement, move again until no more remaining movements
• Determine combat
• Get user command
  - change unit's target or list of targets (location or unit)
  - change attack type or whatever other options are offered

Initial Unit types:
• warrior type class (start with this one for all units including player)
• ranged type class
• support type class
• player unit (it's own class, or one of the others?)
• stealth unit

###---Jonathan is working on---
Gameplay ideas

