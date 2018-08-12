from Card import Soldier, Spell

class TargetSpell(Spell):
    constraint = "any"
    def play(self, player, enemy):
        player.set_spell(self, self.constraint)
        return super().play(player, enemy)
    def cast(self, target):
        pass

class BuffSpell(TargetSpell):
    buff = "attack"
    value = 1
    cost = 1
    name = "Buff"
    constraint = "soldiers"
    @property
    def subtext(self):
        return "+{} {}".format(self.value, self.buff)
    def cast(self, target):
        setattr(target, self.buff, 
            getattr(target, self.buff) + self.value)

class DirectDamageSpell(TargetSpell):
    damage = 1
    cost = 1
    name = "Direct Damage"
    constraint = "any"
    @property
    def subtext(self):
        return "{} damage".format(self.damage)
    @property
    def info(self):
        return "Do {} damage".format(self.damage)
    def cast(self, target):
        target.take_damage(self, self.damage)

class FastForward(Spell):
    cost = 2
    name = "Fast Forward"
    info = "Gain an empty Mana"
    def play(self, player, enemy):
        player._mana = (
            player._mana[0],
            player._mana[1] + 1
        )
        return super().play(player, enemy)

class ReachOut(Spell):
    cost = 1
    name = "Reach Out"
    info = "Touch space"
    def play(self, player, enemy):
        player._mana = (
            player._mana[0] + 3,
            player._mana[1]
        )
        return super().play(player, enemy)

class Mulligan(Spell):
    cost = 2
    name = "Mulligan"
    info = "Return your hand to your deck and draw the same number of cards"
    def play(self, player, enemy):
        i = player.hand.size
        player.deck.cards.extend(player.hand.cards)
        player.deck.shuffle()
        player.hand.clear()
        for _ in range(i):
            player.draw_card()
        return super().play(player, enemy)

class Boi(Soldier):
    attack = 1
    health = 1
    cost = 1
    name = "Monkey"
    info = "A little boi"

class Archer(Soldier):
    attack = 2
    health = 1
    cost = 2
    name = "Archer"
    info = "Deal 1 damage"
    def battlecry(self, player, enemy):
        spell = DirectDamageSpell()
        spell.damage = 1
        player.set_spell(spell, "any")

class Cobra(Soldier):
    attack = 2
    health = 4
    cost = 3
    name = "Cobra"
    info = "Poisonous cobra"
    poison = True

class Raptor(Soldier):
    attack = 3
    health = 2
    cost = 2
    name = "Raptor"
    info = "Kawhi Leonard"

class Yeti(Soldier):
    attack = 4
    health = 5
    cost = 4
    name = "Abominable Snowman"
    display_name = "Abominable\nSnowman"
    info = "Who ya gonna call"

class Firebreath(DirectDamageSpell):
    damage = 5
    cost = 4
    name = "Firebreath"

class Nuke(DirectDamageSpell):
    damage = 10
    cost = 10
    name = "Nuke"

class Sharpsword(BuffSpell):
    buff = "attack"
    value = 3
    cost = 2
    name = "Sharpsword"