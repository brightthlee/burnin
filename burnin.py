# Copyright 2018 Google Inc. All Rights Reserved.

"""
Burn In test loop
python burnin.py --config-file ./burnin.yaml
"""
import clifford
import Queue
import csv
import threading
import time
import subprocess
from clifford.names import *
from foxconn.adb import *
from test_executor import *
from threading import Thread
from clifford.util import timeouts

conf.Declare('usb_endpoints', "USB Endpoints list for DUT", default_value=False)
conf.Declare("fixture_ctrl","Control fixuture and carrier program url", default_value=False)

def adb_find_device(timeout_s, serial_num=None):
  timeout = timeouts.PolledTimeout.FromSeconds(timeout_s)  
  if serial_num is not None:
    adb_connection = find_device_serial(serial_num)
    while(adb_connection is None):
      is_timeout = timeout.HasExpired()
      if is_timeout:
        break
      time.sleep(1)
      adb_connection = find_device_serial(serial_num)
    return adb_connection
  else :
    # do adb wait-for-device
    adb_wait_queue = Queue.Queue()
    adb_wait_thread = threading.Thread(target=Adb().wait_for_device, args=(adb_wait_queue, False))
    adb_wait_thread.daemon = True
    adb_wait_thread.start()
    # adb_wait_thread.join()
    # ret = adb_wait_queue.get()

    while (adb_wait_thread.is_alive()):
      is_timeout = timeout.HasExpired()
      if is_timeout:
        return None
      time.sleep(1)
    return True

def find_device_serial(serial_num):
  p = subprocess.Popen(["adb", "devices"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = p.communicate()
  p.poll()
  devices = [l.split('\t')[0] for l in stdout.strip().splitlines()[1:]]
  for d in devices:
    connection = Adb(d)
    if serial_num == filter(None, connection.check_output(['/home/flex/bin/fct.sh', 'get_serial']).splitlines())[-2]:
      return connection
  return None

def set_EnvSetup_func(test_data, meas_list):
  result = 'Fail'
  index = test_data.state['thread_id']
  Has_Product = subprocess.call([conf.fixture_ctrl,"has_product",str(index)])
  if Has_Product:
    Em_On = subprocess.call([conf.fixture_ctrl,"em_on",str(index)])
    if Em_On:
      Power_On = subprocess.call([conf.fixture_ctrl,"pw_on",str(index)])
      if Power_On:
        Testable = subprocess.call([conf.fixture_ctrl,"testable",str(index)])
        if Testable:
          result = 'Pass'

  if result == 'Pass':
    ret = adb_find_device(3, serial_num=test_data.state['dut_id'])
    if(ret is None):
      result = 'Fail'
    else:
      result = 'Pass'
<<<<<<< HEAD
 
=======

  # result = 'Pass'   # force pass the env setup
  for meas in meas_list:
    _item=meas[0]
    # _validator=meas[1]
    test_data.measurements[_item] = result

def set_BurnIn_func(test_data, meas_list):
  if conf.scan_sn == True:
    # if serial number is the same with adb devices
    #executor = Test_Executor(serial_number=test_data.state['dut_id'])

    # if need to use usb endpoint 
    #usb_endpoint = conf.usb_endpoints.split(' ')[test_data.state['thread_id']]
    #executor = Test_Executor(usb_ep=usb_endpoint)

    # if need to scan all usb deivces
    executor = Test_Executor(find_serial=test_data.state['dut_id'])
  else:
    executor = Test_Executor()
  for meas in meas_list:
    _item=meas[0]
    # _validator=meas[1]
    test_data.measurements[_item] = executor.run(_item)

def Build_Measment_List_From_CSV(CsvFile):
  measurement_list=[]
  with open(CsvFile, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      measurement_list.append(row)
  return measurement_list

def BuildMeasurement(meas_list):
  measurement_list = []
  for idx, meas in enumerate(meas_list):
    _item=meas[0]
    _value=meas[1]
    if _value.find(',') >= 0:
      _validator=tuple(map(int, meas[1].split(',')))
    else:
      _validator=validator_map[_value]

    if isinstance(_validator, (list,tuple,str)):
      measurement_list.append(Measurement(_item).InRange(*_validator).Doc("{} {}".format(idx,_item)))
    else: 
      measurement_list.append(Measurement(_item).WithValidator(_validator).Doc("{} {}".format(idx,_item)))
  return measurement_list

def BuildPhase(phase_name, meas_list, func, timeout):
  @TestPhase(timeout_s=timeout)
  @measures(*BuildMeasurement(meas_list))
  def fn(test_data):
    func(test_data, meas_list)
  fn.code_info.name = phase_name
  return fn

def is_pass(value):
  if value == 'Fail':
    return False
  elif value == 'Pass':
    return True
  else:
    return value

def test_start(index):
  """
  test start function must return a dut id
  Arg:
    index -- thread index for multiple-up test
  Return:
    sn number
  """
  return 'sn_' + str(index)

def teardown(test_data):
  index = test_data.state['thread_id']
  if test_data:
    test_data.logger.info('Running teardown at end of the test')
    
    if test_data.GetTestResult() == "PASS":
      subprocess.call([conf.fixture_ctrl, "OK", str(index)])
    else:
      subprocess.call([conf.fixture_ctrl, "NG", str(index)])
    subprocess.call([conf.fixture_ctrl,"pw_off", str(index) ])
    subprocess.call([conf.fixture_ctrl, "em_off", str(index)])
  else:
    print('init failed or shopfloor error, running teardown')

validator_map={
  'is_pass': is_pass,
  'PASS': is_pass,
  'OK' : is_pass
}

if __name__ == '__main__':

  running_phases = []
  env_list = Build_Measment_List_From_CSV('EnvSetup.csv')
  env_phase = BuildPhase('EnvSetup', env_list, set_EnvSetup_func, 200)
  
  meas_list = Build_Measment_List_From_CSV('RunInTest.csv')
  burnin_phase = BuildPhase('RunInTest', meas_list, set_BurnIn_func, 200)
  
  running_phases.append(env_phase)
  running_phases.append(burnin_phase)

  test = clifford.Test(*running_phases,
       # Some metadata fields, these in particular are used by mfg-inspector,
      # but you can include any metadata fields.
      test_name='BURNIN', test_description='Clifford FATP BURNIN',
      test_version='B_SMT_1.0.4')

  # upload the test result to data server and keep a local copy
  # the local copy is at current_user_home/CliffordLog
  test.AddOutputCallback(UploadResultJSON)

  test.Configure(teardown_function=teardown)

  test.StartExecution(test_start=test_start)
