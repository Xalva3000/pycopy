from datetime import date

from param_getter import ParamGetter


class PlaceManager:
    def __init__(self, source_folder, destination_folder, params: ParamScheme):
        self.schedule = params
        if self.schedule == "daily":
            self.destination = destination_folder + "daily\\"
        elif self.schedule == "weekly":
            self.destination = destination_folder + "weekly\\" + date.today().strftime("%d-%m") + "\\"
        elif self.schedule == "monthly":
            self.destination = destination_folder + "monthly\\" + date.today().strftime("%Y-%m") + "\\"
        elif self.schedule == "once":
            self.destination = destination_folder + "once\\"

        os.makedirs(self.destination, exist_ok=True)
