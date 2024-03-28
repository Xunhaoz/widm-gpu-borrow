import datetime
from models.database import db
from models.User import User
from models.Hardware import Hardware
from models.UsageLog import UsageLog
from sqlalchemy import and_


class UsageLogService:
    def __init__(self, year, week, hardware_id):
        self.year, self.week, self.hardware_id = year, week, hardware_id
        self.prev_year, self.prev_week, self.next_year, self.next_week = self.get_browse_btn(year, week)

        self.table = [[[] for i in range(24)] for j in range(7)]
        self.table_header = []
        self.people_usage_count = {'Idle': 0}

        self.daily_usage_rate = []
        self.people_usage_rate = []
        self.people_usage_rate_people = []
        self.people_usage_rate_usage_rate = []

        self.get_usage_table()
        self.get_daily_usage_rate()
        self.get_people_usage_rate()

    def get_usage_table(self):
        start_date = datetime.datetime.strptime(f"{self.year}-{self.week}-1", "%Y-%W-%w")
        end_date = datetime.datetime.strptime(f"{self.year}-{self.week}-0", "%Y-%W-%w")

        self.table_header = [(start_date + datetime.timedelta(days=d)).strftime("%m/%d") for d in range(7)]

        joined_data = db.session.query(UsageLog, User) \
            .join(User, UsageLog.user_id == User.id) \
            .filter(UsageLog.date.between(start_date - datetime.timedelta(days=1), end_date)) \
            .filter(UsageLog.hardware_id == self.hardware_id) \
            .all()

        for usage_log, user in joined_data:
            self.table[(usage_log.date - start_date.date()).days][usage_log.period].append(user.chinese_name)
            self.people_usage_count[user.chinese_name] = 0

    def get_daily_usage_rate(self):
        for day in self.table:
            person_count = 0
            for period in day:
                for person in period:
                    person_count += 1
            self.daily_usage_rate.append(person_count / 24)

    def get_people_usage_rate(self):
        total_count = 0
        text_style = ['text-primary', 'text-success', 'text-info', 'text-warning', 'text-danger']

        for day in self.table:
            for period in day:
                if not period:
                    total_count += 1
                    self.people_usage_count["Idle"] += 1
                for person in period:
                    total_count += 1
                    self.people_usage_count[person] += 1

        for idx_, (key, value) in enumerate(self.people_usage_count.items()):
            self.people_usage_rate.append({
                'chinese_name': key,
                'usage_rate': value / total_count,
                'style': text_style[idx_]
            })

            self.people_usage_rate_people.append(key)
            self.people_usage_rate_usage_rate.append(value / total_count)

    def get_browse_btn(self, year, week):
        current_date = datetime.datetime.strptime(f"{year}-{week}-1", "%Y-%W-%w")
        prev_week_date = current_date - datetime.timedelta(weeks=1)
        prev_year, prev_week, _ = prev_week_date.isocalendar()
        next_week_date = current_date + datetime.timedelta(weeks=1)
        next_year, next_week, _ = next_week_date.isocalendar()

        return prev_year, prev_week, next_year, next_week
