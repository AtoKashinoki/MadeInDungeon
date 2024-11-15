

from copy import deepcopy
from time import sleep
from src.Object import Player, Enemy
from CodingTools.Definition import Msvcrt
Key = Msvcrt.Key
from src.Engine import ApplicationEngine, Exit
from src import Texture



class GameLoop(ApplicationEngine):

    def __init__(self, d_map, player: Player, enemies: list[Enemy]):
        super().__init__()
        self.d_map = d_map
        self.player = player
        self.enemies = enemies
        self.game_over = False
        self.attacking = list()
        self.attack_f = False

        player.reset_visibility(d_map)
        player.update_visibility(d_map)
        return

    def update_enemies(self):
        if self.player.move:
            [
                enemy.move_process(self.d_map, self.player, self.enemies)
                for enemy in self.enemies
            ]
            self.player.move = False
            ...
        return

    def __update__(self):
        if self.attack_f:
            sleep(0.15)
            self.update_enemies()
            self.render_update_flag = True
            self.attacking = tuple()
            ...

        else:

            if 224 in self.input:
                if Key.Ins in self.input: self.reboot()
                if Key.Del in self.input: raise Exit

            input_keys = "".join([
                Msvcrt.alphabet_dict[_id]
                for _id in self.input
                if _id in Msvcrt.alphabet_dict
            ])

            for i in range(len(self.attacking)):
                self.attacking[i][1] -= 1
                ...
            pre_cou = len(self.attacking)
            self.attacking = [attacking for attacking in self.attacking if attacking[1] > 0]
            if not pre_cou == len(self.attacking):
                self.render_update_flag = True
                ...

            if input_keys in (*self.player.move_range, *self.player.atk_range):
                self.attacking.append([self.player.game_loop_mp(self.d_map, self.enemies, input_keys), 1])
                self.render_update_flag = True
                ...

            self.enemies = [
                enemy
                for enemy in self.enemies
                if enemy.hp > 0
            ]

            if self.d_map[self.player.position[1]][self.player.position[0]] in (-2, -4):
                raise Exit

            if not len(self.attacking) > 0:
                self.update_enemies()

            if self.player.hp <= 0:
                raise Exit

            ...

        return

    def __rendering__(self):
        player = self.player
        player.update_visibility(self.d_map)

        print_map = Texture.convert(deepcopy(player.visibility_map))
        pp = player.position
        print_map[pp.y][pp.x] = "😀"
        [
            print_map[y].__setitem__(x, "👹")
            for x, y in map(lambda x: x.position, self.enemies)
            if not player.visibility_map[y][x] == -101
        ]
        self.attack_f = False
        for attacking in self.attacking:
            for _dir in attacking[0]:
                if print_map[pp.y+_dir[1]][pp.x+_dir[0]] in ("　", "👹"):
                    print_map[pp.y+_dir[1]][pp.x+_dir[0]] = "##"
                    self.attack_f = True
                    ...
                ...
            ...
        texture = "{}" * len(self.d_map[0])

        self.print()
        self.print("Dungeon map")
        [self.print(texture.format(*_line)) for _line in print_map]
        self.print(f"{player.position=}")
        self.print(f"{player.hp=}")
        self.print()
        if player.f_get_key:
            self.print("Get key!")
            player.f_get_key = False
            ...
        if player.f_attack:
            self.print("Player attack!")
            player.f_attack = False
            if player.f_attack_hit:
                self.print("Hit!!")
                player.f_attack_hit = False
                ...
            ...
        for enemy in self.enemies:
            if enemy.f_attack:
                self.print("Enemy attack!!")
                enemy.f_attack = False
                ...
            ...
        return

    ...