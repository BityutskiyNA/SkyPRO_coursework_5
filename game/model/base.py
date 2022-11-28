from game.model.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = ""
    result = ""

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.game_is_running = False
            self.result = "Ничья"
        elif self.player.hp <= 0 and self.enemy.hp > 0:
            self.game_is_running = False
            self.result = "Игрок проиграл"
        elif self.player.hp > 0 and self.enemy.hp <= 0:
            self.game_is_running = False
            self.result = "Игрок победил"
        elif self.player.hp > 0 and self.enemy.hp > 0:
            self.result = "Бой продолжается"
            return True
        return False

    def _stamina_regeneration(self):
        self.player.stamina += self.STAMINA_PER_ROUND
        self.enemy.stamina += self.STAMINA_PER_ROUND
        if self.player.stamina > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        if self.enemy.stamina > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina

    def next_turn(self):
        result = self._check_players_hp()
        if result:
            self._stamina_regeneration()
            self.battle_result += "\n" + self.enemy.hit(self.player)

    def _end_game(self):
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        self.battle_result += "\n" + self.player.hit(self.enemy)
        self.next_turn()

    def player_use_skill(self):
        self.battle_result += self.player.use_skill(self.enemy)
