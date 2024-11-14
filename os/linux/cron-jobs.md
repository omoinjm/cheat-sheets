# Manage CRON jobs

How to manage cron jobs

[link](https://www.freecodecamp.org/news/cron-jobs-in-linux/)

1. Open the crontab file

```bash
crontab -e
```

2. Add the cron job

```bash
*/7 * * * * /path/to/your/program >> /path/to/logfile.log 2>&1

# Save and exit
```

4. Verify the cron job is listed

```bash
crontab -l
```

5. If you set up logging for your cron job, check the log file for recent entries

```bash
tail -f /path/to/logfile.log
```

6. You can check the system log to see if the cron job is running

```bash
grep CRON /var/log/syslog

# or on some systems

grep cron /var/log/cron.log
```

7. Make sure the cron daemon is running

```bash
systemctl status cron

# if it's not running, you can start it with

sudo systemctl start cron
```
