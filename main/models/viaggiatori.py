from django.db import models
from django.contrib import admin
from main.models.characters import Character
import random

from main.utils.mechanics import roll


class Viaggiatore(Character):
    class Meta:
        verbose_name = "Viaggiatore"
        verbose_name_plural = "Viaggiatori"

    player = models.CharField(max_length=128, default="", blank=True)
    destiny = models.PositiveIntegerField(default=0, blank=True)
    is_storyteller = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.rid}"

    def fix(self):
        super().fix()
        if self.is_storyteller:
            self.player = "Gardien des Rêves"
            self.stress_acquired = -1
        if len(self.entrance) > 0:
            entrance = self.entrance.split(', ')
            entrance.sort()
            self.entrance = ", ".join(entrance)

    def randomize(self):
        if self.is_storyteller:
            self.birthhour = roll(12)
            attributes = ["4", "4", "4", "5", "5", "5", "5", "6", "6", "7", "7", "8"]
            random.shuffle(attributes)
            self.attributes = " ".join(attributes)
            all_values = [
                "7",
                "6", "6",
                "5", "5", "5",
                "4", "4", "4", "4",
                "3", "3", "3", "3", "3",
                "2", "2", "2", "2", "2", "2",
                "1", "1", "1", "1", "1", "1", "1"]
            random.shuffle(all_values)
            r = roll(1, 10)
            spots = [1, 3, 6, 8, 6, 4]
            skills = [[], [], [], [], [], []]
            skills[0] = ["-5" for _ in range(6)]
            skills[1] = ["-4" for _ in range(10)]
            skills[2] = ["-3" for _ in range(10)]
            skills[3] = ["-2" for _ in range(16)]
            skills[4] = ["-1" for _ in range(16)]
            skills[5] = ["-1" for _ in range(18)]
            global_val_idx = 0
            cur_val_idx = 0
            cur_set = 0
            while cur_set < 6:
                print(f"Set #{cur_set:1} => {len(skills[cur_set]):3} GVI {global_val_idx:3} {spots[cur_set]:2}")
                while cur_val_idx < spots[cur_set]:
                    skills[cur_set][cur_val_idx] = all_values[global_val_idx]
                    cur_val_idx += 1
                    global_val_idx += 1
                cur_val_idx = 0
                random.shuffle(skills[cur_set])
                cur_set += 1
            self.skills_draconic = " ".join(skills[0])
            self.skills_knowledge = " ".join(skills[1])
            self.skills_specialized = " ".join(skills[2])
            self.skills_peculiar = " ".join(skills[3])
            self.skills_generic = " ".join(skills[4])
            self.skills_weapons = " ".join(skills[5])


class ViaggiatoreAdmin(admin.ModelAdmin):
    from main.utils.mechanics import pre_sim, refix
    ordering = ['-indice', 'name']
    list_display = ['id', 'rid', 'name', "height", "aka", "is_female", "entrance", 'player', 'is_storyteller', 'bug_list', 'color', 'destiny']
    list_editable = ["height", 'color', "is_female", 'destiny', 'is_storyteller', "aka", "entrance"]
    list_filter = ['is_storyteller', "priority"]
    actions = [refix, pre_sim]
