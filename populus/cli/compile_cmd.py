import click

from populus.compilation import (
    compile_project_contracts,
)

from populus.utils.cli import (
    watch_project_contracts,
)
from populus.utils.compat import (
    spawn,
)
from populus.utils.compile import (
    write_compiled_sources,
)

from .main import main


@main.command('compile')
@click.option(
    '--watch',
    '-w',
    is_flag=True,
    help="Watch contract source files and recompile on changes",
)
@click.pass_context
def compile_cmd(ctx, watch):
    """
    Compile project contracts, storing their output in `./build/contracts.json`

    Call bare to compile all contracts or specify contract names or file paths
    to restrict to only compiling those contracts.

    Pass in a file path and a contract name separated by a colon(":") to
    specify only named contracts in the specified file.
    """
    project = ctx.obj['PROJECT']

    compiler_settings = project.config.get('compilation.settings', {})
    _, compiled_contract_data = compile_project_contracts(project, compiler_settings)
    write_compiled_sources(project.compiled_contracts_asset_path, compiled_contract_data)

    if watch:
        thread = spawn(
            watch_project_contracts,
            project=project,
            compiler_settings=compiler_settings,
        )
        thread.join()
