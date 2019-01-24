from foxconn.adb import *
import subprocess

class Test_Executor:
    method_list = []

    def __init__(self, serial_number = None, usb_ep = None, find_serial = None):

        self.method_list = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]

        if serial_number is not None:
            self._sn = serial_number
            self.adb = Adb(serial_number)
        elif usb_ep is not None:
            self.usb_ep = usb_ep
            self.adb = Adb(usb_ep)
        elif find_serial is not None:
            p = subprocess.Popen(["adb", "devices"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            p.poll()
            devices = [l.split('\t')[0] for l in stdout.strip().splitlines()[1:]]
            for d in devices:
                connection = Adb(d)
                if find_serial == connection.check_output(['/home/flex/bin/fct.sh', 'get_serial']).splitlines()[1]:
                    self.adb = connection
                    break
        else:
            self.adb = Adb()

    def run(self, item_names):
        for method in self.method_list[::-1]:
            if method in item_names:
                return getattr(self, method)()

    def TEST_ADB_ROOT(self):
     	    return self.adb.check_output(['/home/flex/bin/fct.sh','get_serial']).splitlines()[1]

    def TEST_PUSH_BURNIN(self):
            return True

    def TEST_START_TO_BURNIN(self):
            return True

    def CAMERA_TEMP_THERMISTOR_SB(self):
            return True

    def CAMERA_TEMP_THERMISTOR_SB_1_1(self):
            return True

    def IMAGE_CAPTURE(self):
            return True

    def IR_LED_ON_50MA(self):
            return True

    def RGB_LED_ALL_ON_10MA(self):
            return True

    def WIFI_RESET_AND_BOOT(self):
            return True

    def BT_RESET_AND_BOOT(self):
            return True

    def TOGGLE_ICR(self):
            return True

    def READ_TEMP_THERMISTOR_SB(self):
            return True

    def READ_TEMP_THERMISTOR_MPP2_SOC(self):
            return True

    def READ_TEMP_THERMISTOR_MPP3_WIFI(self):
            return True

    def AUDIO_STRESS_TEST(self):
            return True

    def Coprocessor_STRESS_TEST(self):
            return True

    def ENV_SET_MID(self):
            return True

    def MEM_STRESS_TEST(self):
            return True

    def ENV_SET_OFF(self):
            return True

    def TEST_PULL_PICTURE(self):
            return True

    def CAMERA_TEMPERATURE_LOW(self):
            return True

    def DPC_WHITE_PIXELS(self):
            return True

    def DARK_MEAN(self):
            return True

    def DARK_STD(self):
            return True

    def DARK_ROW_STD(self):
            return True

    def DARK_COL_STD(self):
            return True

    def DARK_LOCAL_ROW_STD(self):
            return True

    def DARK_LOCAL_COL_STD(self):
            return True

    def CAMERA_TEMPERATURE_HIGH(self):
            return True

    def DPC_WHITE_PIXELS_HIGHTEMP(self):
            return True

    def DARK_MEAN_HIGHTEMP(self):
            return True

    def DARK_STD_HIGHTEMP(self):
            return True

    def DARK_ROW_STD_HIGHTEMP(self):
            return True

    def DARK_COL_STD_HIGHTEMP(self):
            return True

    def DARK_LOCAL_ROW_STD_HIGHTEMP(self):
            return True

    def DARK_LOCAL_COL_STD_HIGHTEMP(self):
            return True

    def SEND_LOG_TO_CAMERA(self):
            return True
