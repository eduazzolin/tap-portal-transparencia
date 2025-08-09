# tap-portaltransparencia

`tap-portaltransparencia` is a Singer tap
for [Portal da Transparencia API](https://api.portaldatransparencia.gov.br/swagger-ui/index.html). Currently, it
supports extracting data from the following endpoints:

- emendas
- emendas/documentos

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Configuration

### Accepted Config Options

| Setting | Required | Default | Description |
|:--------|:--------:|:-------:|:------------|
| auth_token | True | None | The token to authenticate against the API service |
| emendas_config | False | None | Parameters to be sent to the Emendas endpoint |
| emendas_config.ano | False | None | The year to be extracted from the API |
| emendas_config.nome_autor | False | None | The name of the author to be extracted from the API |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-portaltransparencia --about
```

### Source Authentication and Authorization

1. Login at [Portal da Transparencia](https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email)
2. Follow the steps and request an API token for your account.


## Usage

You can easily run `tap-portaltransparencia` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-portaltransparencia --version
tap-portaltransparencia --help
tap-portaltransparencia --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

Prerequisites:

- Python 3.9+
- [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

### Create and Run Tests

Create tests within the `tests` subfolder and
then run:

```bash
uv run pytest
```

You can also test the `tap-portaltransparencia` CLI interface directly using `uv run`:

```bash
uv run tap-portaltransparencia --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-portaltransparencia
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-portaltransparencia --version

# OR run a test ELT pipeline:
meltano run tap-portaltransparencia target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
