# Check Gitlab Runner Jobs

This icinga2 monitoring-script checks how many jobs are in a given state per runner

```
usage: check_gitlab_runner_jobs.py [-h] -u URL [-s JOBSTATE] -t TOKEN -r RUNNER

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     gitlab base url
  -s JOBSTATE, --jobstate JOBSTATE
                        job state (which jobs should be counted)
                        default=running
  -t TOKEN, --token TOKEN
                        gitlab access token
  -r RUNNER, --runner RUNNER
                        runner name:id (multiple separated by comma) format:
                        name:id,name:id
```

# Authors

- Julian Mühmelt
