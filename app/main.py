from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from constants import GRUNDSTUNDEN, BASE_GROSS, DRIVER_BONUS, OVERTIME_PCT, NIGHT_PCT, SAT_PCT, SUN_PCT, HOLIDAY_PCT, SOCIAL_RATE_EMP, TAX_RATE_BY_CLASS, CHURCH_TAX_RATE
from utils import parse_float, euro

class MonthScreen(Screen):
    pass

class TaxScreen(Screen):
    pass

class HoursScreen(Screen):
    pass

class ResultScreen(Screen):
    gross_text = StringProperty("")
    net_text = StringProperty("")
    details_text = StringProperty("")

class WindowManager(ScreenManager):
    pass

class REVGApp(App):
    def build(self):
        return Builder.load_file("main.kv")

    def calculate_salary(self):
        sm = self.root

        # Λήψη τιμών
        month = sm.get_screen("month").ids.month_spinner.text
        grund = GRUNDSTUNDEN.get(month, 0.0)

        tax_class = sm.get_screen("tax").ids.tax_spinner.text
        church_on = sm.get_screen("tax").ids.church_toggle.state == "down"

        total = parse_float(sm.get_screen("hours").ids.total_hours.text)
        night = parse_float(sm.get_screen("hours").ids.night_hours.text)
        sat = parse_float(sm.get_screen("hours").ids.sat_hours.text)
        sun = parse_float(sm.get_screen("hours").ids.sun_hours.text)
        hol = parse_float(sm.get_screen("hours").ids.hol_hours.text)

        base_hourly = BASE_GROSS / grund if grund else 0
        overtime_h = max(0, total - grund)
        overtime_pay = overtime_h * base_hourly * (1 + OVERTIME_PCT)

        night_pay = night * base_hourly * NIGHT_PCT
        sat_pay = sat * base_hourly * SAT_PCT
        sun_pay = sun * base_hourly * SUN_PCT
        hol_pay = hol * base_hourly * HOLIDAY_PCT

        gross = BASE_GROSS + DRIVER_BONUS + overtime_pay + night_pay + sat_pay + sun_pay + hol_pay
        social = gross * SOCIAL_RATE_EMP
        taxable = max(0, gross - social)
        income_tax = taxable * TAX_RATE_BY_CLASS.get(tax_class, 0.16)
        church_tax = income_tax * CHURCH_TAX_RATE if church_on else 0
        net = gross - social - income_tax - church_tax

        # Ενημέρωση αποτελεσμάτων
        result_screen = sm.get_screen("result")
        result_screen.gross_text = euro(gross)
        result_screen.net_text = euro(net)
        result_screen.details_text = (
            f"Ωρομίσθιο: {euro(base_hourly)}\n"
            f"Υπερωρίες: {euro(overtime_pay)}\n"
            f"Νύχτα: {euro(night_pay)}\n"
            f"Σάββατο: {euro(sat_pay)}\n"
            f"Κυριακή: {euro(sun_pay)}\n"
            f"Αργία: {euro(hol_pay)}\n"
            f"Κρατήσεις: {euro(social)}\n"
            f"Φόρος: {euro(income_tax)}\n"
            f"Εκκλησιαστικός: {euro(church_tax)}"
        )
        sm.current = "result"

if __name__ == "__main__":
    REVGApp().run()
