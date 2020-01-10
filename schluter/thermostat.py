class Thermostat():
    def __init__(self, data):
        self._serial_number = data["SerialNumber"]
        self._name = data["Room"]
        self._group_id = data["GroupId"]
        self._group_name = data["GroupName"]
        self._temperature = data["Temperature"]
        self._set_point_temp = data["SetPointTemp"]
        self._manual_temp = data["ManualTemperature"]
        self._is_online = data["Online"]
        self._is_heating = data["Heating"]
        self._max_temp = data["MaxTemp"]
        self._min_temp = data["MinTemp"]
        self._kwh_charge = data["KwhCharge"]
        self._load_measured_watt = data["LoadMeasuredWatt"]
        self._sw_version = data["SWVersion"]
    
    @property
    def serial_number(self):
        return self._serial_number
        
    @property
    def name(self):
        return self._name
    
    @property
    def group_id(self):
        return self._group_id
    
    @property
    def group_name(self):
        return self._group_name
    
    @property
    def temperature(self):
        return round((self._temperature / 100) * 2) / 2 

    @property
    def set_point_temp(self):
        return round((self._set_point_temp / 100) * 2) / 2 
    
    @property
    def manual_temp(self):
        return round((self._manual_temp / 100) * 2) / 2
    
    @property
    def is_online(self):
        return self._is_online
    
    @property
    def is_heating(self):
        return self._is_heating
    
    @property
    def max_temp(self):
        return round((self._max_temp / 100) * 2) / 2
    
    @property
    def min_temp(self):
        return round((self._min_temp / 100) * 2) / 2
    
    @property
    def kwh_charge(self):
        return self._kwh_charge

    @property
    def load_measured_watt(self):
        return self._load_measured_watt

    @property
    def sw_version(self):
        return self._sw_version
