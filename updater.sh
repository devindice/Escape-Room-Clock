cd /home/pi/Escape-Room-Clock/ &&
git remote update &&
git status -uno | grep 'Your branch is behind' &&
git stash &&
git clean -fd &&
git pull &&
for FILE in $(ls -1a | tail -n+3 | grep -v 'scheduler.cron\|logrotate.conf');do
    chown -R pi:pi $FILE;
done &&
chown root:root /home/pi/Escape-Room-Clock/scheduler.cron &&
chown root:root /home/pi/Escape-Room-Clock/logrotate.conf &&
chmod 644 /home/pi/Escape-Room-Clock/scheduler.cron &&
chmod 644 /home/pi/Escape-Room-Clock/logrotate.conf &&
kill $(ps aux | grep python | grep main.py | grep -v grep | awk '{print $2}')
