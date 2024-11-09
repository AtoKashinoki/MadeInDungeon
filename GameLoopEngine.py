

from copy import deepcopy
from time import sleep

from CodingTools.Definition import Msvcrt
Key = Msvcrt.Key
from Engine import ApplicationEngine, Exit
import Texture



class GameLoop(ApplicationEngine):

    def __init__(self, d_map, player):
        super().__init__()
        self.d_map = d_map
        self.player = player
        self.game_over = False
        self.attacking = list()
        return

    def __update__(self):
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

        if input_keys in self.player.move_range:
            self.attacking.append([self.player.game_loop_mp(self.d_map, [], input_keys), self.fps])
            self.render_update_flag = True
            ...

        if self.d_map[self.player.position[1]][self.player.position[0]] == -2:
            raise Exit

        # Enemy processes

        if self.player.hp <= 0:
            raise Exit

        return

    def __rendering__(self):
        player = self.player
        print_map = Texture.convert(deepcopy(self.d_map))
        pp = player.position
        print_map[pp.y][pp.x] = "〇"
        for attacking in self.attacking:
            for _dir in attacking[0]:
                if print_map[pp.y][pp.x] <= "　":
                    print_map[pp.y+_dir[1]][pp.x+_dir[0]] = " # "
                    ...
                ...
            ...
        texture = "{}" * len(self.d_map[0])
        [self.print(texture.format(*_line)) for _line in print_map]
        self.print(player.position)
        return

    ...