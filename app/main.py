# main.py
import sys, traceback

# ---------- Απλό file logging ----------
LOG_FNAME = "revg_log.txt"

def _setup_file_logging():
    try:
        log_dir = None
        try:
            # Διαθέσιμο σε Android αν έχει μπει το recipe 'android'
            from android.storage import app_storage_path  # type: ignore
            log_dir = app_storage_path()
        except Exception:
            log_dir = "/sdcard/Download"
        sys.stderr = open(f"{log_dir}/{LOG_FNAME}", "a", buffering=1)
        sys.stdout = sys.stderr
        print("\n--- REVG app start ---")
    except Exception:
        pass

_setup_file_logging()

# ---------- Safe imports ----------
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.metrics import dp

Snackbar = None
try:
    # Διαφορετικές ονομασίες σε εκδόσεις KivyMD
    from kivymd.uix.snackbar import MDSnackbar as Snackbar  # type: ignore
except Exception:
    try:
        from kivymd.uix.snackbar import Snackbar  # type: ignore
    except Exception:
        Snackbar = None

try:
    from kivymd.app import MDApp  # type: ignore
    USE_MD = True
except Exception as e:
    print("KivyMD not available at import time:", e)
    USE_MD = False

# ---------- Σταθερές / Ρυθμίσεις ----------
# Πίνακας Grundstunden (2025) όπως μου έστειλες στη φωτο
GRUND_2025 = {
    "Ιανουάριος": 179.4,
    "Φεβρουάριος": 156.0,
    "Μάρτιος": 163.8,
    "Απρίλιος": 171.6,
    "Μάιος": 171.6,
    "Ιούνιος": 163.8,
    "Ιούλιος": 179.4,
    "Αύγουστος": 163.8,
    "Σεπτέμβριος": 171.6,
    "Οκτώβριος": 179.4,
    "Νοέμβριος": 156.0,
    "Δεκέμβριος": 179.4,
}
MONTHS = list(GRUND_2025.keys())

# Defaults / Συντελεστές
BASE_GROSS      = 3112.72
DRIVER_BONUS    = 300.00
OVERTIME_PCT    = 0.30
NIGHT_PCT       = 0.25
SAT_PCT         = 0.20
SUN_PCT         = 0.50
HOLIDAY_PCT     = 1.00
SOCIAL_RATE_EMP = 0.20
TAX_RATE_BY_CLASS = {
    "I": 0.16, "II": 0.12, "III": 0.10, "IV": 0.15, "V": 0.25, "VI": 0.30
}
CHURCH_TAX_RATE = 0.09

# ---------- Βοηθητικά ----------
def fnum(s: str) -> float:
    """δέχεται και κόμμα ως δεκαδικό"""
    if not s:
        return 0.0
    return float(s.replace(",", ".").strip())

def show_snack(text: str):
    try:
        if Snackbar:
            Snackbar(text=text, duration=2).open()
        else:
            print("SNACK:", text)
    except Exception:
        print("SNACK-ERR:", text)

# ---------- Screens ----------
class MonthScreen(Screen):
    selected_month = StringProperty(MONTHS[0])
    grund_label = StringProperty(f"Auto Grundstunden: {GRUND_2025[MONTHS[0]]:.1f}")

    def on_pre_enter(self, *args):
        self.ids.sp_month.text = self.selected_month
        self._update_grund(self.selected_month)

    def month_changed(self, value):
        self.selected_month = value
        self._update_grund(value)

    def _update_grund(self, month):
        g = GRUND_2025.get(month, 0.0)
        self.grund_label = f"Auto Grundstunden: {g:.1f}"

class TaxScreen(Screen):
    tax_class = StringProperty("I")
    church_on = BooleanProperty(False)

    def set_class(self, cls):
        self.tax_class = cls

    def set_church(self, state):
        self.church_on = (state == "down")

class HoursScreen(Screen):
    total_hours = StringProperty("")
    night_hours = StringProperty("")
    sat_hours   = StringProperty("")
    sun_hours   = StringProperty("")
    hol_hours   = StringProperty("")

class ResultScreen(Screen):
    # Εμφάνισε συνοπτικά και με λεπτομέρειες
    gross_text = StringProperty("—")
    net_text   = StringProperty("—")
    details    = StringProperty("—")

# ---------- Screen Manager ----------
class Wizard(ScreenManager):
    pass

# ---------- App ----------
class REVGApp(MDApp if USE_MD else App):

    # Κρατάμε επιλογές χρήστη
    month = StringProperty(MONTHS[0])
    tax_class = StringProperty("I")
    church_on = BooleanProperty(False)

    # ώρες
    total_h = NumericProperty(0.0)
    night_h = NumericProperty(0.0)
    sat_h   = NumericProperty(0.0)
    sun_h   = NumericProperty(0.0)
    hol_h   = NumericProperty(0.0)

    def build(self):
        try:
            # Φτιάχνουμε τα screens «στο χέρι» για να μην εξαρτόμαστε από KV.
            sm = Wizard(transition=SlideTransition())

            # --- Screen 1: Μήνας ---
            s1 = MonthScreen(name="month")
            box1 = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
            box1.add_widget(Label(text="Διάλεξε μήνα εργασίας", font_size="18sp", size                text: "I"
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
