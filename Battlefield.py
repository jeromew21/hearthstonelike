class Battlefield:
    max_size = 7
    def __init__(self, player):
        self.soldiers = []
        self.player = player
    def set_enemy(self, enemy):
        self.enemy = enemy
    def add_soldier(self, soldier):
        if self.size < self.max_size:
            self.soldiers.append(soldier)
    def start_turn(self):
        for s in self.soldiers: s.start_turn()
    def end_turn(self):
        for s in self.soldiers: s.end_turn()
    def can_attack(self, index, enemy):
        return index >= 0 and index < self.size and \
            self.soldiers[index].can_attack and \
            (enemy is self.enemy or enemy in self.enemy.battlefield.soldiers)
    def show(self):
        print("Battlefield: {}".format(self.soldiers))
    @property
    def size(self):
        return len(self.soldiers)
    @property
    def full(self):
        return len(self.soldiers) >= self.max_size