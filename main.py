import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, StringProperty
from kivy.storage.jsonstore import JsonStore

STORE_PATH = "activities.json"

class HomeScreen(Screen):
    pass

class ActivitiesScreen(Screen):
    digital_activities = ListProperty([])
    analogue_activities = ListProperty([])
    inside_activities = ListProperty([])
    outside_activities = ListProperty([])

    def on_pre_enter(self):
        store = JsonStore(STORE_PATH)
        if store.exists('lists'):
            self.digital_activities = store.get('lists')['digital']
            self.analogue_activities = store.get('lists')['analogue']
            self.inside_activities = store.get('lists')['inside']
            self.outside_activities = store.get('lists')['outside']
        else:
            self.digital_activities = []
            self.analogue_activities = []
            self.inside_activities = []
            self.outside_activities = []

    def add_activity(self, activity_type, activity):
        activity = activity.strip()
        if activity:
            store = JsonStore(STORE_PATH)
            lists = store.get('lists') if store.exists('lists') else {'digital': [], 'analogue': [], 'inside': [], 'outside': []}
            if activity not in lists[activity_type]:
                lists[activity_type].append(activity)
                store.put('lists', **lists)
            self.on_pre_enter()

    def remove_activity(self, activity_type, activity):
        store = JsonStore(STORE_PATH)
        lists = store.get('lists') if store.exists('lists') else {'digital': [], 'analogue': [], 'inside': [], 'outside': []}
        if activity in lists[activity_type]:
            lists[activity_type].remove(activity)
            store.put('lists', **lists)
        self.on_pre_enter()

class SuggestionScreen(Screen):
    last_suggestion = StringProperty("")
    suggestion = StringProperty("")

    def suggest(self, activity_type):
        store = JsonStore(STORE_PATH)
        lists = store.get('lists') if store.exists('lists') else {'digital': [], 'analogue': [], 'inside': [], 'outside': []}
        activities = lists[activity_type]
        if activities and len(activities) > 1:
            suggestion = random.choice(activities)
            while suggestion == self.last_suggestion:
                suggestion = random.choice(activities)
            self.suggestion = suggestion
            self.last_suggestion = suggestion
        elif activities and len(activities) == 1:
            self.suggestion = activities[0]
            self.last_suggestion = activities[0]
        else:
            self.suggestion = "No activities found!"

class WhatNowApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ActivitiesScreen(name='activities'))
        sm.add_widget(SuggestionScreen(name='suggestion'))
        return sm

if __name__ == '__main__':
    WhatNowApp().run()