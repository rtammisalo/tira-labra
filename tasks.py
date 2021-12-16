from invoke import task


@task
def timer(ctx):
    ctx.run("python3 src/main.py timer", pty=True)


@task(help={"map": "Map file in maps-directory"})
def start(ctx, map="test.map"):
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
