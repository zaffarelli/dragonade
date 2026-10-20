from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
import json


class Profile(models.Model):
    class Meta:
        ordering = ['user']

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    filters = models.TextField(max_length=2048, default='{}', blank=True)

    def __str__(self):
        return self.user.username

    def prepare_model_filters(self, model):
        filters = json.loads(self.filters)
        if model.lower() not in filters:
            filters[model.lower()] = []
        self.filters = json.dumps(filters)
        self.save()

    # filters handling
    def toggle_filter(self, model, f):
        filters = json.loads(self.filters)
        self.prepare_model_filters(model)
        if f not in filters[model.lower()]:
            filters[model.lower()].append(f)
        else:
            filters[model.lower()].remove(f)
        self.filters = json.dumps(filters)
        self.save()

    def check_filters(self, model, items):
        filters = json.loads(self.filters)
        self.prepare_model_filters(model)
        results = []
        for item in items:
            if item["code"] in filters[model.lower()]:
                item["on"] = True
            else:
                item["on"] = False
            results.append(item)
            print(f"Filter found for user: {item}")
        return results


class ProfileAdmin(admin.ModelAdmin):
    ordering = ['user__username']
    list_display = ["id", "user__username", "user", "filters"]
