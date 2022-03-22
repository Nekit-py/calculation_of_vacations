import logging
from datetime import datetime, timedelta
import holidays


logging.basicConfig(level="INFO")
logger = logging.getLogger("Shedule")


class DateException(ValueError):
    pass


class Shedule:
    #Строго под 2022.

    _holidays_limit = 10
    _holidays_counter = 0
    _rus_holidays = holidays.Russia()
    
    def __init__(self, start_date: str, additional: int, travel: int, days: int) -> None:
        self.start_date = start_date
        self.days = days
        self.additional = additional
        self.travel = travel
        self._vocation_end_date = None

    @staticmethod
    def start_date_to_datetime(start_date: str) -> datetime.date:
        try:
            start_date = datetime.strptime(start_date, "%d.%m.%Y").date()
            return start_date
        except ValueError:
            raise DateException
    
    def set_vocation_end_date(self, vocation_end_date) -> None:
        self._vocation_end_date = vocation_end_date

    def get_vocation_end_date(self) -> None:
        _vocation_end_date = self.start_date
        for _ in range(self.days):
            if any((_vocation_end_date.weekday() in (5, 6), _vocation_end_date in self._rus_holidays)):
                if self._holidays_limit > 0:
                    self._holidays_counter += 1
                    self._holidays_limit -= 1

            if _vocation_end_date == datetime.strptime("05.03.2022", "%d.%m.%Y").date():
                self._holidays_limit += 1
            _vocation_end_date += timedelta(days=1)
        _vocation_end_date += timedelta(days=self._holidays_counter)

        if any((self.additional, self.travel)):
            increase_vocation = self.additional + self.travel
            _vocation_end_date += timedelta(days=increase_vocation)
        self.set_vocation_end_date(_vocation_end_date.strftime("%d.%m.%Y"))

    def __str__(self) -> str:
        return f"Последний день отпуска: --> {self._vocation_end_date}\n\n"

