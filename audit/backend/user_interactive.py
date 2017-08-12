from django.contrib.auth import authenticate
from audit import models
from django.conf import settings
import subprocess
import getpass
import random
import string


class UserShell(object):
    def __init__(self, sys_argv):
        self.sys_argv = sys_argv
    
    def auth(self):
        """
        auth function
        True: user object
        False: None
        """
        count = 0
        while count < 3:
            username = input("username:").strip()
            password = getpass.getpass("password:").strip()
            user = authenticate(username=username, password=password)
            if not user:
                count += 1
                print("Invalid username or password")
                continue
            self.user = user
            return True
        else:
            print("too many attempts!")
            return False

    def run_script(self):
        session_obj = models.SessionLog.objects.create(
            account=self.user.account,
            host_user_bind=self.selected_host)
        session_tracker_script = "/bin/bash {} {} ./log/{}"
        session_tracker_script = session_tracker_script.format(
            settings.SESSION_TRACKER_SCRIPT,
            self.get_random_id,
            session_obj.id)
        session_tracker_obj = subprocess.Popen(
            session_tracker_script,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        return session_tracker_obj

    @property
    def get_random_id(self):
        temp_str = string.ascii_lowercase + string.digits
        self.random_id = ''.join(random.sample(temp_str, 12))
        return self.random_id

    def ssh_connect(self):
        cmd = "sshpass -p {} ssh-audit {}@{} -p {} -o StrictHostKeyChecking=no -Z {}"
        cmd = cmd.format(
                self.selected_host.host_user.password,
                self.selected_host.host_user.username,
                self.selected_host.host.ip_addr,
                self.selected_host.host.port,
                self.random_id,
            )
        return subprocess.run(cmd, shell=True)

    def start(self):
        if not self.auth():
            return None
        # # many to many search
        # print(self.user.account.host_user_binds.all())
        index_list = []
        while True:
            host_groups = self.user.account.host_groups.all()
            # groups list
            for i, v in enumerate(host_groups):
                print("%s\t%s[%s]" % (i, v, v.host_user_binds.count()))
                index_list.append(i)
            # UnGroup host
            print("%s\tUnGroup[%s]" % (
                len(host_groups), 
                self.user.account.host_user_binds.count()))
            # Choice host
            choice = input(">").strip()
            if choice.isdigit():
                choice = int(choice)
            host_bind = None
            if choice in index_list:
                host_bind = host_groups[choice].host_user_binds.all()
            if choice == len(host_groups):
                host_bind = self.user.account.host_user_binds.all()
            if not host_bind:
                print("None Host")
                continue
            index_list1 = []
            while True:
                # hostlist print
                for ii, vv in enumerate(host_bind):
                    print("%s\t%s" % (ii, vv))
                    index_list1.append(ii)
                choice1 = input("> UnGroup >")
                if choice1 == 'q':
                    break
                if choice1.isdigit():
                    choice1 = int(choice1)
                if choice1 not in index_list1:
                    continue
                self.selected_host = host_bind[choice1]
                print("selected host ", self.selected_host)
                script_obj = self.run_script()
                ssh_channel = self.ssh_connect()
                print(script_obj.stdout.read(), script_obj.stderr.read())


# get pid
# ps -ef | grep "lxcb9qme62tu" | egrep -v "grep|sshpass" | awk '{print $2}'
