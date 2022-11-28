from flask import Flask, render_template, request, url_for, redirect

from game.model.base import Arena
from game.model.classes import unit_classes
from game.model.equipment import Equipment
from game.model.unit import PlayerUnit, EnemyUnit

heroes = {}
arena = Arena()

app = Flask(__name__)


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    arena.start_game(heroes['player'], heroes['enemy'])
    return render_template("fight.html", heroes=heroes, result="Бой начался", battle_result="")


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        arena.player_hit()
    return render_template("fight.html", heroes=heroes, result=arena.result, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        arena.player_use_skill()
    return render_template("fight.html", heroes=heroes, result=arena.result, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        arena.next_turn()
    return render_template("fight.html", heroes=heroes, result=arena.result, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    envr = Equipment()
    if request.method == "GET":

        result = {
            "header": "Выберите героя",
            "classes": unit_classes.keys(),
            "weapons": envr.get_weapons_names(),
            "armors": envr.get_armors_names(),
        }
        return render_template("hero_choosing.html", result=result)
    else:
        hero = {
            'name': request.form['name'],
            'unit_class': unit_classes[request.form['unit_class']],
            'weapon': envr.get_weapon(request.form['weapon']),
            'armor': envr.get_armor(request.form['armor']),
        }
        heroes.update(player=PlayerUnit(**hero))
        return redirect(url_for("choose_enemy"), 301)


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    envr = Equipment()
    if request.method == "GET":
        result = {
            "header": "Выберите героя",
            "classes": unit_classes.keys(),
            "weapons": envr.get_weapons_names(),
            "armors": envr.get_armors_names(),
        }
        return render_template("hero_choosing.html", result=result)
    else:
        hero = {
            'name': request.form['name'],
            'unit_class': unit_classes[request.form['unit_class']],
            'weapon': envr.get_weapon(request.form['weapon']),
            'armor': envr.get_armor(request.form['armor']),
        }
        heroes.update(enemy=EnemyUnit(**hero))
        return redirect(url_for("start_fight"), 301)


if __name__ == '__main__':
    app.run()
