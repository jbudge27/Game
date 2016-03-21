# Game
Python game stuffs.

# Arena

The arena is the fighting mode. Should be done on encounter, Pokemon meets Final Fantasy style.
Turn based combat. Each turn can have one of several actions
Change element
Attack with weapon
Attack with element
Defend
Use item
Run away (not available for bosses)
One mode for each element - each should promote its own fighting style
Player chooses element and can switch in menu; not changed by environ
Monster element is given by monster type
Screen layout should have all actions available, along with basic stats
Elemental skills are enhanced/reduced by environ
Player selects up to ?five? skills per element
Skills can be passive or active
Skills are unlocked by elemental level
Elemental weaknesses and strengths are given in 3 tiers
Air - earth - fire - water - lightning
Light - dark - sound
Chaos
Each tier does not interact with the others.
Multiple monster battles can happen, each gets their turn
Turns should be stacked in some sort of queue based on speed

# Map

Tile based
Needs different terrain tiles
Types of terrain: 1 for each element
Water
Earth
Air
Fire
Lightning
Light
Dark
Sound
Chaos
Neutral tiles, too. Maybe gradient tiles? Some ambiguity?
Each tile should have a different mana value to draw from in the arena
Needs doors
Must be able to render monsters, player, and items. Maybe special tiles for things?

# Player

Main player stats and menu items
Should have these main stats:
Attack
Defense
Sp. Attack
Sp. Defense
Speed
HP
Level
Experience
And a separate level for the elements:
Water
Earth
Air
Fire
Lightning
Light
Dark
Sound
Chaos
Each elemental level can be given points to when a player levels up.
Should have several equip slots for
Weapon
Armor
Orb
Ring
And a backpack with ?20? Slots for items.

ITEMS
Orbs
These help with elemental skills and/or level
Can store mana for off-environ skillcasting
May boost general spatk or spdef
Rarer?
Off-environ effects should drain mana if passive
General Items
Basic potion healing stuffs
Stat boosting stuffs
Equipment - weapon/armor
For use in equip slots
Should be separate from backpack when equipped
Boosts atk and def, maybe hp

Rings
For more interesting effects
Boost crit chance?
May help with off-element skills, grant special skills, etc.
SKILLS
These can be selected and added to the arena menu out of battle.
?Five? Skills per element unlocked.
Each monster defeated adds basic exp and exp for its element
Can have passive and activated skills for battle
Skills can be gained by
Leveling up an element
Talking to NPCs
Using an item
Beating a given monster
Doing something unique
Should work almost like hearthstone deck building. Choose your skills to be put into the slots available.
Passive skills only work if element is active

ELEMENTS
Water
Promotes sp. Def and healing
Multiple target damage, but smaller
Absorb and reduce damage
Fire
Spatk and burns
Single target high damage stuff
Increase damage effects
Earth
Defense, hp
Neutralizes things like poison, burns, status changes
Slow but high hp
Air
Speed
Multiple attacks for small damage each, but stacks added effects
Bonuses for multiple hits?
Super fast but fragile
evasive
Lightning
Attack
Fast travel?
Affinity with equipments, amplifies effects
Light
Defense, spdef
Heals and neutralizes
Added effects for level gain, but very weak attack
Confusion?
Reveal info about targets?
Dark
Atk, spatk
Causes effects like burn, confusion, poison
Does not give as much exp?
Very weak defenses
Life drain?
Sound
Speed and balance
Multiple attacks and target effects
Good evasion?
Chaos
Random effects, but powerful ones
Reshapes the battlefield?
Increases power but at the cost of control - more randomized effects

STAT GROWTH
This should be affected by the elements a player levels up in. the elements given above affect their given values.
