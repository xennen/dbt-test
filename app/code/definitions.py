import os
import subprocess

from dagster import Definitions, job, op
from dagster_celery_k8s import celery_k8s_job_executor

K8S_RUN_CONFIG = {
    "dagster-k8s/config": {
        "pod_spec_config": {
            "node_selector": {"team": "analytics"},
            "tolerations": [
                {
                    "key": "team",
                    "operator": "Equal",
                    "value": "analytics",
                    "effect": "NoSchedule",
                }
            ],
        }
    }
}


def _run_dbt(command: list[str]) -> None:
    subprocess.run(
        command,
        check=True,
        cwd="/app",
        env=os.environ.copy(),
    )


@op
def dbt_debug() -> None:
    _run_dbt(["dbt", "debug", "--project-dir", "/app", "--profiles-dir", "/app"])


@op
def dbt_show_edna() -> None:
    _run_dbt(
        [
            "dbt",
            "show",
            "--select",
            "test_edna_sample",
            "--project-dir",
            "/app",
            "--profiles-dir",
            "/app",
            "--limit",
            "10",
        ]
    )


@job(executor_def=celery_k8s_job_executor, tags=K8S_RUN_CONFIG)
def dbt_debug_job() -> None:
    dbt_debug()


@job(executor_def=celery_k8s_job_executor, tags=K8S_RUN_CONFIG)
def dbt_show_edna_job() -> None:
    dbt_show_edna()


defs = Definitions(
    jobs=[dbt_debug_job, dbt_show_edna_job],
)
