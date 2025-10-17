# Check Gitlab Push Mirror

This script can check Gitlab Push Mirrors for errors.
It can check all mirrors in a single project with `--project-id`
or all projects in an group with `--group-id`

```
usage: check_gitlab_push_mirror.py [-h] --url URL --access-token ACCESS_TOKEN [--project-id PROJECT_ID] [--group-id GROUP_ID]

check if push mirroring is failing

options:
  -h, --help            show this help message and exit
  --url URL
  --access-token ACCESS_TOKEN
  --project-id PROJECT_ID
                        Project ID
  --group-id GROUP_ID   Group ID
```

# Requirements
```requirements
python-gitlab
```

# Authors

- Martin Neubert
