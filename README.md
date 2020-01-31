# CMAuditd
CMAuditd is a free and open-source GUI designed to be used with Auditd, which is the userspace component to the Linux Auditing System


Requirements

These are some as follow:

1. Auditd, Python must be installed on your Linux (Debian) machine.
2. You have to create an auditd.log file

    root@cybermizz:~# nano /var/log/audit/auditd.log

3. Change the log path from the auditd.conf

    root@cybermizz:~# nano /etc/audit/auditd.conf

    change the log_file path to

    log_file = /var/log/audit/auditd.log

4. Run is as root

    root@cybermizz:~# python cmauditd.py
