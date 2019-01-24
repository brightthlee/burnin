"""adb wrapper class

"""

import os
import subprocess


class Adb(object):
  """Class of adb connection to DUT"""

  def __init__(self, serial=None):
    """Constructor

    Args:
      serial: serial of DUT
    """

    self._serial = serial
    if serial:
      print ("ADB connect to %s" % serial)
      self._command_prefix = ['adb', '-s', serial]
    else:
      self._command_prefix = ['adb']

  def call(self, command, stdin=None, stdout=None, stderr=None):
    """Executes a command via adb connection.

    Args:
      command: A list of strings for command to execute.
      stdin: A file object to override standard input.
      stdout: A file object to override standard output.
      stderr: A file object to override standard error.

    Returns:
      Return code of command.
    """
    return subprocess.call(
        self._command_prefix + ['shell'] + command,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr)

  def check_call(self, command, stdin=None, stdout=None, stderr=None):
    """Executes a command via adb connection and check return code.

    Args:
      command: A list of strings for command to execute.
      stdin: A file object to override standard input.
      stdout: A file object to override standard output.
      stderr: A file object to override standard error.

    Returns:
      Return code of command.
    """
    return subprocess.check_call(
        self._command_prefix + ['shell'] + command,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr)

  def check_output(self, command, stdin=None, stderr=None, log=False):
    """Executes a command via adb connection and return output.

    Args:
      command: A list of strings for command to execute.
      stdin: A file object to override standard input.
      stdout: A file object to override standard output.
      stderr: A file object to override standard error.
      log: If print out command output

    Returns:
      Return output of command.
    """
    output = subprocess.check_output(
        self._command_prefix + ['shell'] + command, stdin=stdin, stderr=stderr)
    if log:
      print(output)
    return output

  def push(self, target_file, dest, log=False):
    """Push a file to DUT through adb.

    Args:
      target_file: the file to be pushed
      dest: destination path to push on DUT
      log: If print out command output

    Returns:
      Return output of command.
    """
    output = subprocess.check_output(
        self._command_prefix + ['push', target_file, dest])
    if log:
      print(output)
    return output

  def push_dir(self, target_dir, dest, log=False):
    """Push all files in a dir to DUT through adb.

    Args:
      target_dir: the dir to be pushed
      dest: destination path to push on DUT
      log: If print out command output

    Returns:
      Return output of command.

    """
    output = ''
    for f in os.listdir(target_dir):
      output += subprocess.check_output(
          self._command_prefix + ['push',
           os.path.join(target_dir, f), dest])
    if log:
      print(output)
    return output

  def pull(self, target_file, dest, log=False):
    """Pull a file from DUT through adb.

    Args:
      target_file: the file to be pulled
      dest: destination path to put the file
      log: If print out command output

    Returns:
      Return output of command.
    """
    output = subprocess.check_output(
        self._command_prefix + ['pull', target_file, dest])
    if log:
      print(output)
    return output

  def sync(self):
    """Send adb shell sync command"""
    subprocess.check_call(self._command_prefix + ['shell', 'sync'])
