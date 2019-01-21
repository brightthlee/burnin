# Copyright 2018 Google Inc. All Rights Reserved.

"""
Burn In test loop
python burnin.py --config-file ./burnin.yaml
"""
import clifford
from clifford.names import *
import csv
import random

def Build_Measment_List_From_CSV(CsvFile):
  measurement_list=[]
  with open(CsvFile, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      measurement_list.append(row)
  return measurement_list

def BuildMeasurement(meas_list):
  measurement_list = []
  for meas in meas_list:
    _item=meas[0]
    _value=meas[1]
    if _value.find(',') >= 0:
      _validator=tuple(map(int, meas[1].split(',')))
    else:
      _validator=validator_map[_value]

    if isinstance(_validator, (list,tuple,str)):
      measurement_list.append(Measurement(
                              '%s' % _item).InRange(*_validator))
    else: 
      measurement_list.append(Measurement(
                              '%s' % _item).WithValidator(_validator))
  return measurement_list

def BuildPhase(phase_name, meas_list):
  @TestPhase(timeout_s=200)
  @measures(*BuildMeasurement(meas_list))
  def fn(test_data):
    for meas in meas_list:
      _item=meas[0]
      _validator=meas[1]
      test_data.measurements[_item] = random.randint(1,10)
  fn.code_info.name = phase_name
  return fn

def is_pass(value):
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

validator_map={
  'is_pass': is_pass,
  'PASS': is_pass,
  'OK' : is_pass
}

if __name__ == '__main__':

  running_phases = []
  meas_list = Build_Measment_List_From_CSV('RunInTest.csv')
  cur_phase=BuildPhase('RunInTest', meas_list)
  running_phases.append(cur_phase)

  test = clifford.Test(*running_phases,
       # Some metadata fields, these in particular are used by mfg-inspector,
      # but you can include any metadata fields.
      test_name='Hello_world', test_description='Clifford Example Test',
      test_version='B_SMT_1.0.4')

  # upload the test result to data server and keep a local copy
  # the local copy is at current_user_home/CliffordLog
  test.AddOutputCallback(UploadResultJSON)

  test.StartExecution(test_start=test_start)
