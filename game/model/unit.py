import random

from abc import ABC, abstractmethod
from typing import Optional

from game.model.classes import UnitClass
from game.model.equipment import Weapon, Armor


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, weapon, armor, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used = False
    @property
    def health_points(self):
        return self.hp  # TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return self.stamina  # TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self, weapon: Weapon):
        # TODO присваиваем нашему герою новое оружие
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # TODO одеваем новую броню
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target) -> int:
        # TODO Эта функция должна содержать:
        #  логику расчета урона игрока
        #  логику расчета брони цели
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        self.stamina -= self.weapon.stamina_per_hit
        weapon_dm = round(random.uniform(1.5, 5.5), 2)
        attack_pw = (weapon_dm * self.unit_class.attack) - target.armor.defence

        if target.stamina >= target.armor.stamina_per_turn:
            armor_target = target.armor.defence * target.unit_class.armor
        else:
            armor_target = 0

        damage = attack_pw-armor_target

        if damage > 0:
            return damage
        else:
            return 0


    def get_damage(self, damage: int) -> Optional[int]:
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        self.hp -= damage

    @abstractmethod
    def hit(self, target) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return "Навык использован"
        else:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if not self.stamina >= self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        # if not self.weapon.damage
        damage = self._count_damage(target)

        # # TODO результат функции должен возвращать следующие строки:
        if damage == 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            target.get_damage(damage)
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."




class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if random.randrange(1, 10) == 7:
            return self.use_skill(target)
        else:
            if not self.stamina >= self.weapon.stamina_per_hit:
                return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
            damage = self._count_damage(target)

            if damage == 0:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
            else:
                target.get_damage(damage)
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
