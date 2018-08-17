from copy import deepcopy

def score(player):
    if player.health <= 0:
        return -30
    return (player.health/2
        + sum([c.health + c.attack for c in player.battlefield.soldiers]))

class AI:
    def __init__(self, game, n):
        self.game = game
    def make_turn(self):
        game = self.game
        original = game.player2
        hand_cache = []
        null_score = score(game.player2) - score(game.player1)
        for i, _ in enumerate(game.player2.hand.cards):
            game_ = deepcopy(game)
            game_.player1.say = lambda s: None
            game_.player2.say = lambda s: None
            player = game_.player2
            moves = []
            hand_cache.append(moves)
            if player.play_card(i):
                moves.append(('card', i))
                if player.spell:
                    best = 0
                    best_score = -100
                    for i, _ in enumerate(player.spell_targets):
                        g = deepcopy(game_)
                        p = g.player2
                        p.cast(p.spell_targets[i])
                        sc = score(p) - score(g.player1)
                        if sc > best_score:
                            best = i
                            best_score = sc
                    moves.append(('target', best))
                    moves.append(('end', best_score))
                else:
                    moves.append(('end', score(player) - score(game_.player1)))
        
        for moves in sorted(hand_cache, key=lambda k: k[-1][1] if k else 0):
            if not moves:
                continue
            if moves[-1][1] < null_score:
                continue
            for action, index in moves:
                if action == "card":
                    original.play_card(index)
                elif action == "target":
                    if original.spell_targets:
                        original.cast(original.spell_targets[index])

        for i, _ in enumerate(game.player2.battlefield.soldiers):
            best = 'base'
            best_score = -100
            for f, k in enumerate(game.player1.battlefield.soldiers + ["base"]):
                g = deepcopy(game)
                g.player1.say = lambda s: None
                g.player2.say = lambda s: None
                p = game.player2
                if k == 'base':
                    p.soldier_attack(i, g.player1) 
                else:
                    if f >= 0 and f < g.player1.battlefield.size:
                        p.soldier_attack(i, g.player1.battlefield.soldiers[f])
                sc = score(p) - score(g.player1)
                if sc > best_score:
                    best = 'base' if k == 'base' else f
                    best_score = sc
            if best == 'base':
                original.soldier_attack(i, game.player1)
            else:
                if best >= 0 and best < game.player1.battlefield.size:
                    original.soldier_attack(i, game.player1.battlefield.soldiers[best])
