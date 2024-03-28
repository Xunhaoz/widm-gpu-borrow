import datetime
from models.Hardware import Hardware
from models.User import User


class BarService:
    def __init__(self, ncu_protal):
        self.machines = []
        self.machine_gpu_map = {}  # one to many pair
        self.id_gpu_map = {}  # one to one
        self.id_machine_map = {}  # one to one

        self.user_id = ""
        self.user_chinese_name = ""
        self.user_email = ""
        self.user_ncu_protal = ncu_protal

        self.now_year = datetime.datetime.now().year
        self.now_week = datetime.datetime.now().isocalendar().week

        self.get_hardware()
        self.get_user()

    def get_hardware(self):
        hardwares = Hardware.query.all()
        for hardware in hardwares:
            if hardware.machine not in self.machine_gpu_map:
                self.machine_gpu_map[hardware.machine] = []
                self.machines.append(hardware.machine)
            self.id_gpu_map[hardware.id] = hardware.gpu
            self.id_machine_map[hardware.id] = hardware.machine
            self.machine_gpu_map[hardware.machine].append((hardware.gpu, hardware.id))
        self.machines = sorted(self.machines)

    def get_user(self):
        if self.user_ncu_protal is None:
            return

        user = User.query.filter_by(token=self.user_ncu_protal).first()
        self.user_id = user.id
        self.user_chinese_name = user.chinese_name
        self.user_email = user.email