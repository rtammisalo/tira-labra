from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/main.py")


@task
def timer(ctx):
    ctx.run("python3 src/main.py timer")


@task
def pytest(ctx):
    ctx.run("pytest", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
