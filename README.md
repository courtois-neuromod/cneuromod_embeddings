# cneuromod-embeddings

This [book](https://courtois-neuromod.github.io/cneuromod_embeddings/) presents a series of experiment to validate the quality of individual dynamic brain parcellations in the Courtois NeuroMod (CNeuroMod) data sample, including a variety of tasks and movies. 

## Usage

### Building the book

If you'd like to develop on and build the cneuromod-embeddings book, you should:

- Clone this repository and run
- Run `pip install -r requirements.txt` (it is recommended you do this within a virtual environment)
- Run `pip install -e .` (this will install the cneuromod_embeddings python module)
- (Recommended) Remove the existing `cneuromod-embeddings/_build/` directory
- Run `jupyter-book build cneuromod-embeddings/`

A fully-rendered HTML version of the book will be built in `cneuromod-embeddings/_build/html/`.

### Hosting the book

The html version of the book is hosted on the `gh-pages` branch of this repo. Navigate to your local build and run,
- `ghp-import -n -p -f book/_build/html`

This will automatically push your build to the `gh-pages` branch. More information on this hosting process can be found [here](https://jupyterbook.org/publish/gh-pages.html#manually-host-your-book-with-github-pages).

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/pbellec/cneuromod_embeddings/graphs/contributors).

## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
