from datetime import date
import os

from param_getter import ParamScheme


class PlaceManager:
    def __init__(self, params: ParamScheme):
        self.schedule = params.schedule
        destination_folder = params.destination_folder

        if self.schedule == "daily":
            self.destination = destination_folder + "daily\\"
        elif self.schedule == "weekly":
            self.destination = destination_folder + "weekly\\" + date.today().strftime("%d-%m") + "\\"
        elif self.schedule == "monthly":
            self.destination = destination_folder + "monthly\\" + date.today().strftime("%Y-%m") + "\\"
        elif self.schedule == "once":
            self.destination = destination_folder + "once\\"

    def create_if_not_exists(self):
        os.makedirs(self.destination, exist_ok=True)
        return self.destination

    def remove_similar(self, lst):
        for file_name in lst:
            os.remove(self.destination + file_name)
