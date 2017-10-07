import sys

from fabric.state import env

# import winrm.winrm_service
import winrm
import os

class WinRMWebServiceWrapper(object):
    def __init__(self, host, username, password, timeout=None, port=5986):
        self.client = winrm.Session( "https://{0}:{1}/wsman".format(host, port), auth=(username, password), server_cert_validation='ignore',operation_timeout_sec=230, read_timeout_sec=240)
        # if timeout is not None:
        #     self.client.set_timeout(timeout)
        # else:
        #     self.client.set_timeout(3600)

    def exec_command(self, command):
        # shell_id = self.client.open_shell()
        return self.client.run_ps(command)
        # return _WinRMCommandWrapper(self.client, command_id)


   


# class _WinRMCommandWrapper(object):
#     """Wrapper around a single winrm command to ensure proper cleanup."""
#     def __init__(self, client, command_id):
#         self.client = client
#         self.shell_id = shell_id
#         self.command_id = command_id
#
#     def cleanup(self):
#         self.client.cleanup_command(self.shell_id, self.command_id)
#         self.client.close_shell(self.shell_id)
#
#     def get_command_output(self):
#         return self.client.get_command_output(self.shell_id, self.command_id)
#
#     def _raw_get_command_output(self):
#         return self.client._raw_get_command_output(self.shell_id, self.command_id)
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, *a, **kw):
#         self.cleanup()

def execute_winrm_command(host, command, combine_stderr=None, stdout=None,
        stderr=None, timeout=None, user=None, password=None, port=5986):
    # stdout/stderr redirection
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr

    if combine_stderr is None:
        combine_stderr = env.combine_stderr

    if user is None:
        user = env.user
    if password is None:
        password = env.password

    invoke_shell = False
    remote_interrupt = False

    winrm_service = WinRMWebServiceWrapper(host, user, password, timeout=timeout, port=port)

    winrm_command = winrm_service.exec_command(command=command)

    stdout_buffer = winrm_command.std_out
    stderr_buffer = winrm_command.std_err
    status =  winrm_command.status_code


    # is_done = False
    # while not is_done:
    #     _stdout, _stderr, status, is_done = winrm_command._raw_get_command_output()
    #     for (buf, stream, prefix) in ((_stdout, stdout, "out"), (_stderr, stderr, "err")):
    #         lines = buf.splitlines()
    #         for line in lines[:-1]:
    #             stream.write("[{}] {}: {}\n".format(env.host_string, prefix, line))
    #         if lines:
    #             if buf.endswith("\n"):
    #                 suffix = "\n"
    #             else:
    #                 suffix = ""
    #             stream.write("[{}] {}: {}{}".format(env.host_string, prefix, lines[-1], suffix))
    #
    # # Update stdout/stderr with captured values if applicable
    # if not invoke_shell:
    #     stdout_buf = ''.join(_stdout).strip()
    #     stderr_buf = ''.join(_stderr).strip()
    # else:
    #     raise NotImplementedError()

    return stdout_buffer, stderr_buffer, status

