#!/usr/bin/env python3

"""
Copyright 2025-2025 Deutsche Telekom MMS GmbH
Maintainer: Martin Neubert
check if push mirroring is failing
"""

import argparse
import sys
import gitlab


class State:
    name: str
    weight: int

    def __init__(self, project, mirror):
        self.project = project
        self.mirror = mirror

    def __str__(self):
        return f"[{self.name}] Project {self.project.name_with_namespace} Push Mirror {self.mirror.url} is {self.mirror.update_status}"


class StateOk(State):
    name: str = "OK"
    weight: int = 0


class StateWarning(State):
    name: str = "WARNING"
    weight: int = 1


class StateCritical(State):
    name: str = "CRITICAL"
    weight: int = 2


def check_mirrors(project) -> list[State]:
    states: list[State] = []
    for mirror in project.remote_mirrors.list(get_all=True):
        if mirror.last_error is not None or mirror.update_status == "failed":
            states.append(StateCritical(project, mirror))
        else:
            states.append(StateOk(project, mirror))
    return states


def main():
    parser = argparse.ArgumentParser(
        prog="check_gitlab_push_mirror.py",
        description="check if push mirroring is failing",
    )

    parser.add_argument("--url", required=True)
    parser.add_argument("--access-token", required=True)
    parser.add_argument("--project-id", help="Project ID")
    parser.add_argument("--group-id", help="Group ID")

    args = parser.parse_args()

    # login to gitlab with private token
    try:
        gl = gitlab.Gitlab(f"https://{args.url}", args.access_token)
    except gitlab.GitlabAuthenticationError:
        print("login with private token failed")
        sys.exit(255)

    states: list[State] = []

    if args.project_id:
        project = gl.projects.get(args.project_id, active=True)
        states.extend(check_mirrors(project))
    elif args.group_id:
        group = gl.groups.get(args.group_id, lazy=True, active=True)
        for project in group.projects.list(
            get_all=True, lazy=True, include_subgroups=True, active=True
        ):
            project = gl.projects.get(project.id)
            if project.permissions.get("group_access"):
                states.extend(check_mirrors(project))
    else:
        print("Group ID or Project ID are required")
        sys.exit(255)

    states.sort(key=lambda s: s.weight, reverse=True)
    for state in states:
        print(state)

    if any(isinstance(s, StateCritical) for s in states):
        sys.exit(2)
    if any(isinstance(s, StateWarning) for s in states):
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
