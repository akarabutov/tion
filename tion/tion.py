import requests
from os import path
from time import time, sleep

class TionConnection:
    def __init__(self, data: dict):
        self.state = data.get("state")  # connected
        self.is_online = data.get("is_online")  # True
        self.last_seen_iso = data.get("last_seen_iso")  # 2019-03-09T09:16:50.2467772Z
        self.last_seen = data.get("last_seen")  # 1552123010
        self.last_packet_time_iso = data.get("last_packet_time_iso")  # 2019-03-09T09:16:50.2467772Z
        self.last_packet_time = data.get("last_packet_time")  # 1552123010
        self.data_state = data.get("data_state")  # valid
        self.last_seen_delta = data.get("last_seen_delta")  #

    def __repr__(self):
        return f"""TionConnection
        state = {self.state}
        is_online = {self.is_online}
        last_seen_iso = {self.last_seen_iso}
        last_seen = {self.last_seen}
        last_packet_time_iso = {self.last_packet_time_iso}
        last_packet_time = {self.last_packet_time}
        data_state = {self.data_state}
        last_seen_delta = {self.last_seen_delta}
        """


class TionUpdate:
    def __init__(self, data: dict):
        self.state = data.get("state")  # no
        self.device_type = data.get("device_type")  # unknown
        self.mac = data.get("mac")  #
        self.mac_human = data.get("mac_human")  # 00:00:00:00:00:00
        self.progress = data.get("progress")  #

    def __repr__(self):
        return f"""TionUpdate
        state = {self.state}
        device_type = {self.device_type}
        mac = {self.mac}
        mac_human = {self.mac_human}
        progress = {self.progress}
        """


class TionZonesModeAutoSet:
    def __init__(self, data: dict):
        self.co2 = data.get("co2")  # 801.0
        self.temperature = data.get("temperature")  #
        self.humidity = data.get("humidity")  #
        self.noise = data.get("noise")  #
        self.pm25 = data.get("pm25")  #
        self.pm10 = data.get("pm10")  #

    def __repr__(self):
        return f"""TionZonesModeAutoSet
        co2 = {self.co2}
        temperature = {self.temperature}
        humidity = {self.humidity}
        noise = {self.noise}
        pm25 = {self.pm25}
        pm10 = {self.pm10}
        """


class TionZonesMode:
    def __init__(self, data: dict):
        self.current = data.get("current")  # auto
        self.auto_set = TionZonesModeAutoSet(data.get("auto_set", {}))

    def __repr__(self):
        return f"""TionZonesMode
        current = {self.current}
        auto_set = TionZonesModeAutoSet()
        """


class TionZonesScheduleCurrentPreset:
    def __init__(self, data: dict):
        self.preset_id = data.get("preset_id")  # e31502e2-ee3e-49af-aeb6-752d03a428e4
        self.name = data.get("name")  # День
        self.icon = data.get("icon")  # 1
        self.starts_at = data.get("starts_at")  # 1552176300

    def __repr__(self):
        return f"""TionZonesScheduleCurrentPreset
        preset_id = {self.preset_id}
        name = {self.name}
        icon = {self.icon}
        starts_at = {self.starts_at}
        """


class TionZonesSchedule:
    def __init__(self, data: dict):
        self.is_schedule_sync = data.get("is_schedule_sync")  # True
        self.is_active = data.get("is_active")  # True
        self.is_mode_sync = data.get("is_mode_sync")  # True
        self.current_preset = TionZonesScheduleCurrentPreset(data.get("current_preset", {}))
        self.next_preset_starts_at = data.get("next_preset_starts_at")  # 1552176300
        self.next_starts_iso = data.get("next_starts_iso")  # 2019-03-10T00:05:00.0000000Z

    def __repr__(self):
        return f"""TionZonesSchedule
        is_schedule_sync = {self.is_schedule_sync}
        is_active = {self.is_active}
        is_mode_sync = {self.is_mode_sync}
        current_preset = TionZonesScheduleCurrentPreset()
        next_preset_starts_at = {self.next_preset_starts_at}
        next_starts_iso = {self.next_starts_iso}
        """


class TionZonesSensorsAverageData:
    def __init__(self, data: dict):
        self.co2 = data.get("co2")  # 418.0
        self.temperature = data.get("temperature")  # 25.1
        self.humidity = data.get("humidity")  # 23.88
        self.pm25 = data.get("pm25")  # NaN
        self.pm10 = data.get("pm10")  # NaN
        self.radon = data.get("radon")  #
        self.measurement_time_iso = data.get("measurement_time_iso")  # 2019-03-09T09:16:52.0000000
        self.measurement_time = data.get("measurement_time")  # 1552123012

    def __repr__(self):
        return f"""TionZonesSensorsAverageData
        co2 = {self.co2}
        temperature = {self.temperature}
        humidity = {self.humidity}
        pm25 = {self.pm25}
        pm10 = {self.pm10}
        radon = {self.radon}
        measurement_time_iso = {self.measurement_time_iso}
        measurement_time = {self.measurement_time}
        """


class TionZonesSensorsAverage:
    def __init__(self, data: dict):
        self.data_type = data.get("data_type")  # co2th
        self.have_sensors = data.get("have_sensors")
        self.data = TionZonesSensorsAverageData(data.get("data", {}))

    def __repr__(self):
        return f"""TionZonesSensorsAverage
        data_type = {self.data_type}
        have_sensors = [] ({len(self.have_sensors)} items)
        data = TionZonesSensorsAverageData()
        """


class TionZones:
    def __init__(self, data: dict):
        self.guid = data.get("guid")  # edf54e75-9a3a-4cf4-9265-808be2d0e5e9
        self.name = data.get("name")  # Гостиная
        self.type = data.get("type")  # unkown
        self.color = data.get("color")  # 00ccff
        self.is_virtual = data.get("is_virtual")  #
        self.mode = TionZonesMode(data.get("mode", {}))
        self.schedule = TionZonesSchedule(data.get("schedule", {}))
        self.sensors_average = []
        for item in data.get("sensors_average", []):
            self.sensors_average.append(TionZonesSensorsAverage(item))
        self.hw_id = data.get("hw_id")  # 859996424
        self.devices = []
        for item in data.get("devices", []):
            self.devices.append(TionZonesDevices(item))
        self.order = data.get("order")  # 2
        self.creation_time_iso = data.get("creation_time_iso")  # 2019-03-05T10:27:31.7207231Z
        self.creation_time = data.get("creation_time")  # 1551781651
        self.update_time_iso = data.get("update_time_iso")  # 2019-03-05T10:27:31.7207231Z
        self.update_time = data.get("update_time")  # 1551781651

    def __repr__(self):
        return f"""TionZones
        guid = {self.guid}
        name = {self.name}
        type = {self.type}
        color = {self.color}
        is_virtual = {self.is_virtual}
        mode = TionZonesMode()
        schedule = TionZonesSchedule()
        sensors_average = [] ({len(self.sensors_average)} items)
        hw_id = {self.hw_id}
        devices = [] ({len(self.devices)} items)
        order = {self.order}
        creation_time_iso = {self.creation_time_iso}
        creation_time = {self.creation_time}
        update_time_iso = {self.update_time_iso}
        update_time = {self.update_time}
        """


class TionZonesDevicesDataPairing:
    def __init__(self, data: dict):
        self.stage = data.get("stage")  # off
        self.time_left = data.get("time_left")  #
        self.pairing_result = data.get("pairing_result")  #
        self.mac = data.get("mac")  # 00:00:00:00:00:00
        self.device_type = data.get("device_type")  # unknown
        self.subtype = data.get("subtype")  # 0000
        self.subtype_d = data.get("subtype_d")  #

    def __repr__(self):
        return f"""TionZonesDevicesDataPairing
        stage = {self.stage}
        time_left = {self.time_left}
        pairing_result = {self.pairing_result}
        mac = {self.mac}
        device_type = {self.device_type}
        subtype = {self.subtype}
        subtype_d = {self.subtype_d}
        """


class TionZonesDevicesData:
    def __init__(self, data: dict):
        self.status = data.get("status")  # application
        self.wi_fi = data.get("wi-fi")  # 120
        self.pairing = TionZonesDevicesDataPairing(data.get("pairing", {}))
        self.co2 = data.get("co2")  # 418.0
        self.temperature = data.get("temperature")  # 25.1
        self.humidity = data.get("humidity")  # 23.88
        self.pm25 = data.get("pm25")  # NaN
        self.pm10 = data.get("pm10")  # NaN
        self.signal_level = data.get("signal_level")  # 157
        self.backlight = data.get("backlight")  # 1
        self.reliability_code = data.get("reliability_code")  # 0x00000007
        self.last_seen_iso = data.get("last_seen_iso")  # 2019-03-09T09:16:52.0000000
        self.last_seen = data.get("last_seen")  # 1552123012
        self.measurement_time_iso = data.get("measurement_time_iso")  # 2019-03-09T09:16:52.0000000
        self.measurement_time = data.get("measurement_time")  # 1552123012
        self.is_on = data.get("is_on")  #
        self.data_valid = data.get("data_valid")  # True
        self.heater_installed = data.get("heater_installed")  # True
        self.heater_enabled = data.get("heater_enabled")  # True
        self.speed = data.get("speed")  # 1.0
        self.speed_m3h = data.get("speed_m3h")  #
        self.speed_max_set = data.get("speed_max_set")  # 2
        self.speed_min_set = data.get("speed_min_set")  #
        self.speed_limit = data.get("speed_limit")  # 6.0
        self.t_in = data.get("t_in")  # 22.0
        self.t_set = data.get("t_set")  # 20.0
        self.t_out = data.get("t_out")  # 23.0
        self.gate = data.get("gate")  # 2
        self.run_seconds = data.get("run_seconds")  # 179293
        self.filter_time_seconds = data.get("filter_time_seconds")  # 30996247
        self.rc_controlled = data.get("rc_controlled")  #
        self.filter_need_replace = data.get("filter_need_replace")  #
        self.errors = TionZonesDevicesDataErrors(data.get("errors", {}))

    def __repr__(self):
        return f"""TionZonesDevicesData
        status = {self.status}
        wi_fi = {self.wi_fi}
        pairing = TionZonesDevicesDataPairing()
        co2 = {self.co2}
        temperature = {self.temperature}
        humidity = {self.humidity}
        pm25 = {self.pm25}
        pm10 = {self.pm10}
        signal_level = {self.signal_level}
        backlight = {self.backlight}
        reliability_code = {self.reliability_code}
        last_seen_iso = {self.last_seen_iso}
        last_seen = {self.last_seen}
        measurement_time_iso = {self.measurement_time_iso}
        measurement_time = {self.measurement_time}
        is_on = {self.is_on}
        data_valid = {self.data_valid}
        heater_installed = {self.heater_installed}
        heater_enabled = {self.heater_enabled}
        speed = {self.speed}
        speed_m3h = {self.speed_m3h}
        speed_max_set = {self.speed_max_set}
        speed_min_set = {self.speed_min_set}
        speed_limit = {self.speed_limit}
        t_in = {self.t_in}
        t_set = {self.t_set}
        t_out = {self.t_out}
        gate = {self.gate}
        run_seconds = {self.run_seconds}
        filter_time_seconds = {self.filter_time_seconds}
        rc_controlled = {self.rc_controlled}
        filter_need_replace = {self.filter_need_replace}
        errors = TionZonesDevicesDataErrors()
        """


class TionZonesDevices:
    def __init__(self, data: dict):
        self.guid = data.get("guid")  # 9289c923-5665-4fd1-8259-28ce45668a81
        self.name = data.get("name")  # Tion Breezer 3S 1
        self.type = data.get("type")  # breezer3
        self.subtype_d = data.get("subtype_d")  #
        self.control_type = data.get("control_type")  # rf
        self.mac = data.get("mac")  # 3A:BE:65:DF:0C:C2
        self.mac_long = data.get("mac_long")  # 213360543383098
        self.is_online = data.get("is_online")  # True
        self.last_seen_delta = data.get("last_seen_delta")  #
        self.zone_hwid = data.get("zone_hwid")  # 859996424
        self.serial_number = data.get("serial_number")  #
        self.order = data.get("order")  # 1
        self.data = TionZonesDevicesData(data.get("data", {}))
        self.firmware = data.get("firmware")  # 0036
        self.hardware = data.get("hardware")  # 0001
        self.creation_time = data.get("creation_time")  # 1551783681
        self.update_time = data.get("update_time")  # 1551783777
        self.temperature_control = data.get("temperature_control")  # absolute
        self.max_speed = data.get("max_speed")  # 6
        self.t_max = data.get("t_max")  # 30.0
        self.t_min = data.get("t_min")  #

    def __repr__(self):
        return f"""TionZonesDevices
        guid = {self.guid}
        name = {self.name}
        type = {self.type}
        subtype_d = {self.subtype_d}
        control_type = {self.control_type}
        mac = {self.mac}
        mac_long = {self.mac_long}
        is_online = {self.is_online}
        last_seen_delta = {self.last_seen_delta}
        zone_hwid = {self.zone_hwid}
        serial_number = {self.serial_number}
        order = {self.order}
        data = TionZonesDevicesData()
        firmware = {self.firmware}
        hardware = {self.hardware}
        creation_time = {self.creation_time}
        update_time = {self.update_time}
        temperature_control = {self.temperature_control}
        max_speed = {self.max_speed}
        t_max = {self.t_max}
        t_min = {self.t_min}
        """


class TionZonesDevicesDataErrors:
    def __init__(self, data: dict):
        self.code = data.get("code")  # 0x00000000

    def __repr__(self):
        return f"""TionZonesDevicesDataErrors
        code = {self.code}
        list = [] ({len(self.list)} items)
        """


class Tion:
    def __init__(self, data: dict):
        self.guid = data.get("guid")  # 9c5e1f19-36ed-4b26-8c11-5d1b4bf37b91
        self.name = data.get("name")  # Дом
        self.comment = data.get("comment")  #
        self.timezone = data.get("timezone")  # 10800
        self.type = data.get("type")  # unknown
        self.access_level = data.get("access_level")  # owner
        self.repository = data.get("repository")  # production
        self.mac = data.get("mac")  # 28:34:02:39:38:51
        self.connection = TionConnection(data.get("connection", {}))
        self.update = TionUpdate(data.get("update", {}))
        self.unique_key = data.get("unique_key")  # 99b5b792-fa65-47ac-8ee9-cdb39ed58ccd
        self.replace_in_progress = data.get("replace_in_progress")  #
        self.struct_received = data.get("struct_received")  # True
        self.order = data.get("order")  #
        self.zones = []
        for item in data.get("zones", []):
            self.zones.append(TionZones(item))
        self.creation_time_iso = data.get("creation_time_iso")  # 2019-03-05T10:11:15.6830422Z
        self.creation_time = data.get("creation_time")  # 1551780675
        self.update_time_iso = data.get("update_time_iso")  # 2019-03-05T10:11:15.6830422Z
        self.update_time = data.get("update_time")  # 1551780675

    def __repr__(self):
        return f"""Tion
        guid = {self.guid}
        name = {self.name}
        comment = {self.comment}
        timezone = {self.timezone}
        type = {self.type}
        access_level = {self.access_level}
        repository = {self.repository}
        mac = {self.mac}
        connection = TionConnection()
        update = TionUpdate()
        unique_key = {self.unique_key}
        replace_in_progress = {self.replace_in_progress}
        struct_received = {self.struct_received}
        order = {self.order}
        zones = [] ({len(self.zones)} items)
        creation_time_iso = {self.creation_time_iso}
        creation_time = {self.creation_time}
        update_time_iso = {self.update_time_iso}
        update_time = {self.update_time}
        """


class Zone:
    def __init__(self, zone: TionZones, api):
        self.api = api
        self.guid = None
        self.name = None
        self.mode = None
        self.target_co2 = None
        self.load(zone)

    def __repr__(self):
        return f"Zone({self.name}, mode={self.mode}, valid={self.valid})"

    def load(self, zone_data: TionZones=None) -> bool:
        if not zone_data:
            zones = self.api._get_zones_data(guid=self.guid)
            if zones:
                zone_data = zones[0]
        self.guid = zone_data.guid
        self.name = zone_data.name
        self.mode = zone_data.mode.current
        self.target_co2 = zone_data.mode.auto_set.co2
        return self.valid

    def send(self) -> bool:
        if not self.valid:
            return False
        data = {
            "mode": self.mode if self.mode in ("auto", "manual") else "manual",
            "co2": int(self.target_co2)
        }
        url = f"https://api2.magicair.tion.ru/zone/{self.guid}/mode"
        js = requests.post(url, json=data, headers=self.api.headers).json()
        status = js["status"]
        if status != "queued":
            print("TionApi auto set " + status + ": " + js["description"])
            return False
        return True

    @property
    def valid(self):
        return None not in [value for __, value in self.__dict__.items()]


class MagicAir(TionZonesDevices):
    def __init__(self, device: TionZonesDevices, zone: Zone, api):
        self.name = device.name
        self.guid = device.guid
        self.zone = zone
        self.api = api
        self.co2 = None
        self.temperature = None
        self.humidity = None
        self.load(device)

    def __repr__(self):
        return f"MagicAir({self.name}, valid = {self.valid})"

    @property
    def valid(self):
        return None not in [value for __, value in self.__dict__.items()]

    def load(self, device_data: TionZonesDevices=None):
        if not device_data:
            devices = self.api.get_devices(guid=self.guid)
            if devices:
                device_data = devices[0]
        data: TionZonesDevicesData = device_data.data
        self.co2 = data.co2
        self.temperature = data.temperature
        self.humidity = data.humidity
        return self.valid


class Breezer(TionZonesDevices):
    def __init__(self, device: TionZonesDevices, zone: Zone, api):
        self.name = device.name
        self.guid = device.guid
        self.zone = zone
        self.api = api
        self.t_in = None
        self.t_out = None
        self.filter_need_replace = None
        self.data_valid = None
        self.is_on = None
        self.heater_enabled = None
        self.t_set = None
        self.speed = None
        self.speed_min_set = None
        self.speed_max_set = None
        self.load(device)

    def __repr__(self):
        return f"Breezer({self.name}, valid = {self.valid})"

    def send(self) -> bool:
        if not self.valid:
            return False
        data = {
            "is_on": bool(self.is_on),
            "heater_enabled": bool(self.heater_enabled),
            "t_set": int(self.t_set + 0.5),
            "speed": int(self.speed + 0.5),
            "speed_min_set": int(self.speed_min_set + 0.5),
            "speed_max_set": int(self.speed_max_set + 0.5)
        }
        url = f"https://api2.magicair.tion.ru/device/{self.guid}/mode"
        js = requests.post(url, json=data, headers=self.api.headers).json()
        status = js["status"]
        if status != "queued":
            print("TionApi parameters set " + status + ": " + js["description"])
            return False
        return True

    @property
    def valid(self):
        return None not in [value for __, value in self.__dict__.items()] and self.data_valid

    def load(self, device_data: TionZonesDevices=None):
        if not device_data:
            devices, _ = self.api._get_devices_data(guid=self.guid)
            if devices:
                device_data = devices[0]
        data: TionZonesDevicesData = device_data.data
        self.data_valid = data.data_valid
        self.is_on = data.is_on
        self.heater_enabled = data.heater_enabled
        self.t_set = data.t_set
        self.speed = data.speed
        self.speed_min_set = data.speed_min_set
        self.speed_max_set = data.speed_max_set
        self.t_in = data.t_in
        self.t_out = data.t_out
        self.filter_need_replace = data.filter_need_replace
        return self.valid


class TionApi:
    auth_fname = "tion_auth"

    def __init__(self, email: str, password: str, save_auth=True):
        self._email = email
        self._password = password
        self._save_auth = save_auth
        if self._save_auth and path.exists(TionApi.auth_fname):
            with open(TionApi.auth_fname) as file:
                self.authorization = file.read()
        else:
            self.authorization = None
            self._get_authorization()
        self._last_update = 0
        self._data: Tion = None
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ru-RU",
            "Authorization": self.authorization,
            "Connection": "Keep-Alive",
            "Content-Type": "application/json",
            "Host": "api2.magicair.tion.ru",
            "Origin": "https://magicair.tion.ru",
            "Referer": "https://magicair.tion.ru/dashboard/overview",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586"
        }
        self.get_data()

    def __repr__(self):
        return f"TionApi({self.authorization}, data={'Tion()' if self._data else None})"

    def _get_authorization(self):
        data = {
            "username": self._email,
            "password": self._password,
            "client_id": "cd594955-f5ba-4c20-9583-5990bb29f4ef",
            "client_secret": "syRxSrT77P",
            "grant_type": "password"
        }
        try:
            response = requests.post("https://api2.magicair.tion.ru/idsrv/oauth2/token", data=data)
            if response.status_code == 200:
                js = response.json()
                self.authorization = f"{js['token_type']} {js['access_token']}"
                if self._save_auth:
                    with open(TionApi.auth_fname, "w") as file:
                        file.write(self.authorization)
                print("Got new token")
                return True
            else:
                print(f"Status code while getting token: {response.status_code}!")
                return False
        except Exception as e:
            print(f"Exception while getting token!\n{e}")
            return False

    def get_data(self) -> Tion:
        if (time() - self._last_update) < 1:  # update only once per second
            return True
        url = "https://api2.magicair.tion.ru/location"
        self._data = None
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                self._data: Tion = Tion(response.json()[0])
                self._last_update = time()
                return True
            else:
                if response.status_code == 401:
                    if self._get_authorization():
                        return self.get_data()
                    else:
                        print("Authorization failed!")
                else:
                    print("Status code while getting data is {response.status_code}!")
                return False
        except Exception as e:
            print(f"Exception while getting data!\n{e}")
            return False


    def _get_zones_data(self, name_part: str=None, guid: str=None) -> list:
        result = []
        if self.get_data():
            for zone in self._data.zones:
                if any([
                    not name_part and not guid,
                    guid and zone.guid == guid,
                    name_part and name_part.lower() in zone.name.lower()
                        ]):
                    result.append(zone)
        return result

    def get_zones(self, name_part: str=None, guid: str=None) -> list:
        zones_data = self._get_zones_data(name_part, guid)
        result = []
        for zone_data in zones_data:
            result.append(Zone(zone_data, self))
        return result

    def _get_devices_data(self, name_part: str=None, guid: str=None, type: str=None) -> list:
        devices_data = []
        zones = []
        if self.get_data():
            for zone in self._data.zones:
                for device in zone.devices:
                    if any([
                            not name_part and not guid and not type,
                            guid and device.guid == guid,
                            name_part and name_part.lower() in device.name.lower(),
                            type and type.lower() in device.type.lower()
                           ]):
                        devices_data.append(device)
                        zones.append(zone)
        return devices_data, zones

    def get_devices(self, name_part: str=None, guid: str=None, type: str=None) -> list:
        devices_data, zones = self._get_devices_data(name_part, guid, type)
        result = []
        for device_data, zone in zip(devices_data, zones):
            if "co2" in device_data.type:
                result.append(MagicAir(device_data, zone, self))
            elif "breezer" in device_data.type:
                result.append(Breezer(device_data, zone, self))
            else:
                assert False, f"Unknown device type {device_data.type}!"
        return result

"""
import os
from time import sleep
from tion import TionApi, Breezer, Zone, MagicAir
# initialization api
email, password = os.environ.get("TION_AUTH").split(',')
api = TionApi(email, password)
# getting current co2 level from magicair
magicair = api.get_devices(name_part="magic")[0]
print(magicair.co2)
sleep(3)
# setting manual mode for zone Гостиная
zone = api.get_zones(name_part="Гостиная")[0]
zone.mode = "manual"
zone.send()
sleep(3)
zone.load()
assert zone.mode == "manual"  # making sure that mode is set correctly
# turning off breezer
breezer = api.get_devices(name_part="breezer")[0]
breezer.is_on = False
breezer.send()
sleep(3)
breezer.load()
assert zone.mode == "manual"  # making sure that mode is set correctly
# setting auto mode for zone Гостиная
zone.mode = "auto"
zone.send()
sleep(3)
zone.load()
assert zone.mode == "auto"
# setting breezer minimum speed to 3 and maximum to 6
breezer.speed_min_set = 3
breezer.speed_max_set = 6
breezer.send()
sleep(3)
breezer.load()
assert breezer.speed_min_set == 3
"""