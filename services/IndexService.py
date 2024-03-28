import datetime
from models.database import db
from models.Hardware import Hardware
from models.UsageLog import UsageLog
from models.User import User


class IndexService:
    def __init__(self):
        self.current_date = datetime.date.today()
        self.first_day_of_month = None
        self.last_day_of_month = None
        self.hardware_usage = []

        self.current_using = []
        self.current_idling = []

        self.get_date_range()
        self.get_monthly_usage()
        self.get_current_machine_status()

    def get_date_range(self):
        self.first_day_of_month = self.current_date.replace(day=1)
        if self.current_date.month == 12:
            next_month = 1
            next_year = self.current_date.year + 1
        else:
            next_month = self.current_date.month + 1
            next_year = self.current_date.year
        next_month_first_day = datetime.date(next_year, next_month, 1)
        self.last_day_of_month = next_month_first_day - datetime.timedelta(days=1)

    def get_monthly_usage(self):
        def usage_style_mapping(usage_rate):
            if usage_rate < 20:
                return 'bg-danger'
            elif usage_rate < 40:
                return 'bg-warning'
            elif usage_rate < 60:
                return ''
            elif usage_rate < 80:
                return 'bg-info'
            elif usage_rate < 100:
                return 'bg-success'

        hardware_usage_payload = {}
        for hardware in Hardware().query.all():
            hardware_usage_payload[f"{hardware.machine} - {hardware.gpu}"] = 0

        usage_logs = db.session.query(UsageLog, Hardware) \
            .join(Hardware, UsageLog.hardware_id == Hardware.id) \
            .filter(UsageLog.date.between(self.first_day_of_month, self.last_day_of_month)) \
            .all()

        for usage_log, hardware in usage_logs:
            hardware_usage_payload[f"{hardware.machine} - {hardware.gpu}"] += 1

        for k, v in hardware_usage_payload.items():
            hardware_usage_payload[k] = round(v * 100 / 744, 2)

            self.hardware_usage.append({
                'hardware': k,
                'usage': hardware_usage_payload[k],
                'style': usage_style_mapping(hardware_usage_payload[k])
            })

    def get_current_machine_status(self):
        for hardware in Hardware.query.all():
            self.current_idling.append(f"{hardware.machine} - {hardware.gpu}")

        usage_logs = db.session.query(UsageLog, Hardware, User) \
            .join(Hardware, UsageLog.hardware_id == Hardware.id) \
            .join(User, UsageLog.user_id == User.id) \
            .filter(UsageLog.date == datetime.datetime.now().date()) \
            .filter(UsageLog.period == datetime.datetime.now().hour) \
            .all()

        for user_log, hardware, user in usage_logs:
            self.current_using.append({
                "hardware": f"{hardware.machine} - {hardware.gpu}",
                "user": user.chinese_name,
            })
            self.current_idling.remove(f"{hardware.machine} - {hardware.gpu}")
