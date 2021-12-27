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
def csv(ctx):
    ctx.run(f"python3 src/main.py csv", pty=True)


@task(help={"map": "Map file"})
def dijkstra(ctx, map=os.path.join("maps", "test.map")):
    ctx.run(f"python3 src/main.py dijkstra {map}", pty=True)


@task(help={"map": "Map file"})
def jps(ctx, map=os.path.join("maps", "test.map")):
    ctx.run(f"python3 src/main.py jps {map}", pty=True)


@task(help={"map": "Map file"})
def idastra(ctx, map=os.path.join("maps", "test.map")):
    ctx.run(f"python3 src/main.py idastar {map}", pty=True)


@task
def pytest(ctx):
    ctx.run("pytest", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
