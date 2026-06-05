import os
import subprocess

from dagster import Definitions, job, op


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


@job
def dbt_debug_job() -> None:
    dbt_debug()


@job
def dbt_show_edna_job() -> None:
    dbt_show_edna()


defs = Definitions(
    jobs=[dbt_debug_job, dbt_show_edna_job],
)
