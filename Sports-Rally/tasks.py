from invoke import task

@task
def start(ctx):
    ctx.run("python src/main.py", pty=False)

@task
def test(ctx):
    ctx.run("pytest src", pty=False)


@task
def lint(ctx):
    ctx.run("pylint src", pty=False)


@task
def format(ctx):  # pylint: disable=redefined-builtin
    ctx.run("autopep8 --in-place --recursive src", pty=False)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=False)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=False)

#@task
#def build(ctx):
    #ctx.run("python3 src/build.py", pty=True) 