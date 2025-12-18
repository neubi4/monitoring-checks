# Check GitLab Jobs

This script checks the status of a specific GitLab CI/CD job. It retrieves the last 100 jobs from a GitLab project and monitors the status of the most recent job matching the provided job name.

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

```bash
./check_gitlab_jobs.py -u <GITLAB_URL> -p <PROJECT_ID> -t <TOKEN> -j <JOB_NAME>
```

### Example

```bash
./check_gitlab_jobs.py -u https://gitlab.example.com -p 123 -t glpat-xxxxxxxxxxxx -j deploy_qa
```

## Parameters

| Parameter | Short | Description | Required |
|-----------|-------|-------------|----------|
| `--gitlab_url` | `-u` | GitLab instance URL (e.g., https://gitlab.example.com) | Yes |
| `--projectid` | `-p` | GitLab project ID | Yes |
| `--token` | `-t` | GitLab private token with API access | Yes |
| `--jobname` | `-j` | Name of the job to check (exact match) | Yes |

## Exit Codes

| Code | Status | Description |
|------|--------|-------------|
| 0 | OK | Job status is 'success' or job not found in last 100 jobs |
| 1 | WARNING | Job status is 'running' or 'pending' |
| 2 | CRITICAL | Job status is 'failed', 'canceled', 'skipped', or any other non-success status |

## Examples

### Success Status

```
OK - Job: deploy_qa, Job-ID: 12345, Status: success, URL: https://gitlab.example.com/project/repo/-/jobs/12345
```

**Exit Code:** 0

### Running/Pending Status

```
WARNING - Job: deploy_qa, Job-ID: 12346, Status: running, URL: https://gitlab.example.com/project/repo/-/jobs/12346
```

**Exit Code:** 1

### Failed Status

```
CRITICAL - Job: deploy_qa, Job-ID: 12347, Status: failed, URL: https://gitlab.example.com/project/repo/-/jobs/12347
```

**Exit Code:** 2

### Job Not Found

```
OK - Job 'deploy_qa' not found in last 100 jobs
```

**Exit Code:** 0

## Notes

- The script retrieves the last 100 jobs ordered by ID (most recent first)
- Only the most recent job matching the exact job name is checked
- If a job is not found in the last 100 jobs, the check returns OK (useful for jobs that don't run regularly)
- The script uses exact name matching, not substring matching

## Authors

- Sebastian Wolschke
