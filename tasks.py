from invoke import task


@task
def timer(ctx):
    ctx.run("python3 src/main.py timer", pty=True)

@task
def start(ctx):
    ctx.run("python3 src/main.py", pty=True)

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
