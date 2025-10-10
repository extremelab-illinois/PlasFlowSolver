# Examples: layout, local runs, and CI smoke

This directory contains examples of PlasFlowSolver cases.  These examples are used for local sanity checks
and by CI testing.

Each example case lives in `examples/exampleN/` and runs **non-interactively** via a case-specific `script.pfs`.

---

## Minimal scenario structure

Each `exampleN/` must contain:

```text
examples/
  example1/
    script.pfs                 # <- drives a non-interactive run
    example.srun               # <- input (copied from example_files)
    database_settings.pfs      # <- input (copied from example_files)
    mixtures   -> ../../mixtures    # <- resource symlink
    thermo     -> ../../thermo      # <- resource symlink
    transport  -> ../../transport   # <- resource symlink
```

- `script.pfs` selects the "srun" mode and the input file:

```text
Mode: srun
File: example.srun
Settings: N/A
```

- **Resource directories** are symlinks pointing back to PlasFlowSolver's top-level folders. Keep these three links for now.


---

## Run locally

Here's a quick guide on how to run the example cases locally by hand.

From the repo root:

```bash
cd examples/example1
python -u ../../main.py
```

The expected outputs are:
- `db_example.h5`
- `example_db.csv`
- `example_out.srun`

Quick check:
```bash
ls -lh db_example.h5 example_db.csv example_out.srun
```

-----

## What CI does

1. Discovers `examples/example*` directories
2. For each example, verifies the required inputs and links exist
3. Runs `python -u ../../main.py` inside the example directory
4. Asserts:
  - exit code is 0;
  - outputs `db_example.h5`, `example_db.csv`, `example_out.srun` exist and are non-empty.
5. Prints a short tail of the run log on failure (i.e. if the test fails)

## Adding a new case

1. Create a unique directory `examples/exampleX`  (X is an integer)
2. Copy (or craft new) inputs:
   - script.pfs
   - example.srun
   - database_settings.pfs
3. Add resource symlinks from inside `examples/exampleX`
   ```bash
   ln -s ../../mixtures   mixtures
   ln -s ../../thermo     thermo
   ln -s ../../transport  transport
   ```
4. Run locally and confirm the three outputs are produced.
5. Commit the directory:
   ```bash
   git add examples/exampleX
   git commit -m 'Add exampleX showing blah blah blah'
   ```

If you're adding or modifying examples and something seems brittle, open an issue and tag it with
`examples` and `CI`.
