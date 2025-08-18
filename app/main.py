# main.py
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from constants import *
from utils import parse_float, euro

KV = """
MDScreenManager:
    MDScreen:
        name: "month"
        MDBoxLayout:
            orientation: "vertical"
            spacing: "10dp"
            MDLabel:
                text: "Διάλεξε μήνα εργασίας"
            MDDropDownItem:
                id: month_item
                text: "Ιαν"
                on_release: app.select_month()
            MDLabel:
                id: grund_label
                text: "Auto: 172.71 ώρες"
            MDRaisedButton:
                text: "Επόμενο"
                on_release: app.root.current = "tax"

    MDScreen:
        name: "tax"
        MDBoxLayout:
            orientation: "vertical"
            MDLabel:
                text: "Φορολογική κλάση"
            MDDropDownItem:
                id: class_item
                text: "I"
                on_release: app.select_class()
            MDLabel:
                text: "Εκκλησιαστικός φόρος"
            MDSwitch:
                id: church_switch
            MDRaisedButton:
                text: "Επόμενο"
                on_release: app.root.current = "hours"

    MDScreen:
        name: "hours"
        MDBoxLayout:
            orientation: "vertical"
            MDTextField:
                id: total_hours
                hint_text: "Συνολικές ώρες"
            MDTextField:
                id: night_hours
                hint_text: "Ώρες νύχτας"
            MDTextField:
                id: sat_hours
                hint_text: "Ώρες Σαββάτου"
            MDTextField:
                id: sun_hours
                hint_text: "Ώρες Κυριακής"
            MDTextField:
                id: hol_hours
                hint_text: "Ώρες Αργίας"
            MDRaisedButton:
                text: "Δείξε αποτελέσματα"
                on_release: app.show_results()

    MDScreen:
        name: "results"
        MDBoxLayout:
            orientation: "vertical"
            MDLabel:
                id: gross_label
                text: "Μικτό:"
            MDLabel:
                id: net_label
                text: "Καθαρό:"
            MDRaisedButton:
                text: "Πίσω"
                on_release: app.root.current = "hours"
"""


class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def select_month(self):
        # TODO: dropdown logic
        pass

    def select_class(self):
        # TODO: dropdown logic
        pass

    def show_results(self):
        total = parse_float(self.root.get_screen("hours").ids.total_hours.text)
        gross = BASE_GROSS
        net = gross * (1 - SOCIAL_RATE_EMP)
        self.root.get_screen("results").ids.gross_label.text = f"Μικτό: {euro(gross)}"
        self.root.get_screen("results").ids.net_label.text = f"Καθαρό: {euro(net)}"
        self.root.current = "results"


if __name__ == "__main__":
    MainApp().run()
