from dataclasses import dataclass

from game.model.skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(name="Воин",
                         max_health=20.0,
                         max_stamina=20.0,
                         attack=2.0,
                         stamina=2.0,
                         armor=20.0,
                         skill=FuryPunch())

ThiefClass = UnitClass(name="Вор",
                       max_health=10.0,
                       max_stamina=20.0,
                       attack=1.0,
                       stamina=2.0,
                       armor=10.0,
                       skill=HardShot())

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
