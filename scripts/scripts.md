# SCRIPTS

1. render_randomforest.sh

Run the render_randomforest.sh script to render the randomforest.qmd file to a html and pdf file. This script will also start a preview server on the default port 4343.

Run the script:

```bash
./scripts/render_randomforest.sh
```

Open the preview server in your browser:

```bash
open http://localhost:4343
```

Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

Deactivate the Python virtual environment:

```bash
deactivate
```

Clear cached memory to help preserve system memory and RAM (requires sudo privileges):

```bash
sudo sync; sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```


