import os
from invoke import task


@task(help={"map": "Map file"})
def timer(ctx, map=None):
    if map:
        ctx.run(f"python3 src/main.py timer {map}", pty=True)
    else:
        ctx.run("python3 src/main.py timer", pty=True)


@task(help={"map": "Map file"})
def start(ctx, map=os.path.join("maps", "test.map")):
    ctx.run(f"python3 src/main.py {map}", pty=True)


@task
def dijkstra(ctx):
    ctx.run("python3 src/main.py dijsktra", pty=True)


@task
def jps(ctx):
    ctx.run("python3 src/main.py jps", pty=True)


@task
def pytest(ctx):
    ctx.run("pytest", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
