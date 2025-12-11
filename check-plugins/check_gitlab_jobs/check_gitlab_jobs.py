#!/usr/bin/env python3
# -*- coding: utf-8 *-*

"""
Copyright 2025 Deutsche Telekom MMS GmbH
Maintainer: Sebastian Wolschke
"""

import sys
import argparse
from argparse import RawDescriptionHelpFormatter
import requests


def check_gitlab_jobs(
    gitlab_url: str,
    project_id: str,
    token: str,
    job_name: str,
) -> None:
    """Checks the status of a specific GitLab job"""
    client = requests.Session()
    client.headers.update({'PRIVATE-TOKEN': token})

    url = (
        f"{gitlab_url}/api/v4/projects/{project_id}/jobs"
        f"?per_page=100&order_by=id&sort=desc"
    )

    try:
        r = client.get(url, timeout=60)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        print(f"CRITICAL - Unable to connect to GitLab URL '{gitlab_url}': {err}")
        sys.exit(2)
    except requests.exceptions.Timeout as err:
        print(f"CRITICAL - Connection timeout while reaching GitLab URL '{gitlab_url}': {err}")
        sys.exit(2)
    except requests.exceptions.HTTPError as err:
        if r.status_code == 401:
            print(f"CRITICAL - Access denied: Invalid or unauthorized token for GitLab URL '{gitlab_url}'")
        elif r.status_code == 404:
            print(f"CRITICAL - Project not found: Project ID '{project_id}' does not exist or you don't have access to it")
        else:
            print(f"CRITICAL - HTTP Error: {err}")
        sys.exit(2)
    except requests.exceptions.JSONDecodeError as err:
        print(f"CRITICAL - unable to decode JSON from the HTTP Response: {err}")
        sys.exit(2)

    jobs = r.json()

    # Find the first (most recent) job matching the job name
    for job in jobs:
        if job['name'] == job_name:
            job_id = job['id']
            status = job['status']
            web_url = job['web_url']

            if status == 'success':
                print(
                    f"OK - Job: {job_name}, Job-ID: {job_id}, "
                    f"Status: {status}, URL: {web_url}"
                )
                sys.exit(0)
            elif status in ['running', 'pending']:
                print(
                    f"WARNING - Job: {job_name}, Job-ID: {job_id}, "
                    f"Status: {status}, URL: {web_url}"
                )
                sys.exit(1)
            else:
                print(
                    f"CRITICAL - Job: {job_name}, Job-ID: {job_id}, "
                    f"Status: {status}, URL: {web_url}"
                )
                sys.exit(2)

    # Job not found in last 100 jobs
    print(f"OK - Job '{job_name}' not found in last 100 jobs")
    sys.exit(0)


def main() -> None:
    """Entrypoint"""
    parser = argparse.ArgumentParser(
        prog="Check Gitlab Jobs",
        description="""This script checks the status of a specific GitLab job.
It retrieves the last 100 jobs from a project and checks the status of the
most recent job matching the provided job name. The check returns OK if the
job status is 'success' or if the job is not found, WARNING if the job is
'running' or 'pending', and CRITICAL for any other status (failed, canceled,
skipped, etc.).""",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("-u", "--gitlab_url", dest="gitlab_url", required=True)
    parser.add_argument("-p", "--projectid", dest="project_id", required=True)
    parser.add_argument("-t", "--token", dest="token", required=True)
    parser.add_argument(
        "-j",
        "--jobname",
        dest="job_name",
        required=True,
        help="The name of the job to check"
    )
    args = parser.parse_args()

    check_gitlab_jobs(
        args.gitlab_url,
        args.project_id,
        args.token,
        args.job_name,
    )


if __name__ == "__main__":
    main()
