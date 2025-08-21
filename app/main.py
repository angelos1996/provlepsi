# main.py
import sys
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

from constants import (
    GRUNDSTUNDEN, BASE_GROSS, DRIVER_BONUS, OVERTIME_PCT, NIGHT_PCT, SAT_PCT, 
    SUN_PCT, HOLIDAY_PCT, SOCIAL_RATE_EMP, TAX_RATE_BY_CLASS, CHURCH_TAX_RATE
)
from utils import parse_float, euro

MONTHS = list(GRUNDSTUNDEN.keys())

# Υπολογισμός μισθού
def calculate_salary(month, total_h, night_h, sat_h, sun_h, hol_h, tax_class, church_on):
    grund = GRUNDSTUNDEN.get(month, 0.0)
    base_hourly = BASE_GROSS / grund if grund > 0 else 0.0

    overtime_h = max(0, total_h - grund)
    overtime_pay = overtime_h * base_hourly * (1 + OVERTIME_PCT)

    night_pay = night_h * base_hourly * NIGHT_PCT
    sat_pay = sat_h * base_hourly * SAT_PCT
    sun_pay = sun_h * base_hourly * SUN_PCT
    hol_pay = hol_h * base_hourly * HOLIDAY_PCT

    gross = BASE_GROSS + DRIVER_BONUS + overtime_pay + night_pay + sat_pay + sun_pay + hol_pay
    social = gross * SOCIAL_RATE_EMP
    taxable = max(0, gross - social)
    income_tax = taxable * TAX_RATE_BY_CLASS.get(tax_class.upper(), 0.16)
    church_tax = income_tax * CHURCH_TAX_RATE if church_on else 0.0
    net = gross - social - income_tax - church_tax

    return {
        "gross": round(gross, 2),
        "net": round(net, 2),
        "details": {
            "base_hourly": round(base_hourly, 2),
            "overtime_h": overtime_h,
            "overtime_pay": round(overtime_pay, 2),
            "night_pay": round(night_pay, 2),
            "sat_pay": round(sat_pay, 2),
            "sun_pay": round(sun_pay, 2),
            "hol_pay": round(hol_pay, 2),
            "social": round(social, 2),
            "income_tax": round(income_tax, 2),
            "church_tax": round(church_tax, 2),
            "driver_bonus": DRIVER_BONUS,
            "grund": grund
        }
    }

# Screens
class MonthScreen(Screen):
    selected_month = StringProperty(MONTHS[0])
    grund_label = StringProperty("")

    def on_pre_enter(self):
        self.ids.month_spinner.text = self.selected_month
        self.update_label(self.selected_month)

    def update_label(self, month):
        grund = GRUNDSTUNDEN.get(month, 0.0)
        self.grund_label = f"Grundstunden: {grund:.1f}"

    def month_changed(self, text):
        self.selected_month = text
        self.update_label(text)

class TaxScreen(Screen):
    tax_class = StringProperty("I")
    church_on = BooleanProperty(False)

    def set_tax_class(self, val):
        self.tax_class = val

    def set_church(self, state):
        self.church_on = (state == "down")

class HoursScreen(Screen):
    total = StringProperty("")
    night = StringProperty("")
    sat   = StringProperty("")
    sun   = StringProperty("")
    hol   = StringProperty("")

class ResultScreen(Screen):
    gross_result = StringProperty("—")
    net_result   = StringProperty("—")
    details_text = StringProperty("—")

# App
class ScreenController(ScreenManager):
    pass

class REVGApp(App):
    def build(self):
        self.sm = ScreenController(transition=SlideTransition())
        self.sm.add_widget(MonthScreen(name="month"))
        self.sm.add_widget(TaxScreen(name="tax"))
        self.sm.add_widget(HoursScreen(name="hours"))
        self.sm.add_widget(ResultScreen(name="result"))
        return self.sm

    def get_data_and_calculate(self):
        month_screen = self.sm.get_screen("month")
        tax_screen   = self.sm.get_screen("
