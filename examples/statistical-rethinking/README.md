# statistical rethinking

- [Amazon](https://a.co/d/1cBf3Vp)
- [Author's Book Webpage](https://xcelab.net/rm/statistical-rethinking/)
- [Course 2023 - Github](https://github.com/rmcelreath/stat_rethinking_2023)
    - [Course 2022 - Github](https://github.com/rmcelreath/stat_rethinking_2022)
- [Github for PyMC Version](https://github.com/pymc-devs/pymc-resources/tree/main/Rethinking_2)
- [My original Github repo in R](https://github.com/shane-kercheval/r-examples/tree/main/examples/statistical-rethinking)

# Environment

These notebooks are developed and executed within a docker container. See `Makefile` commands for building the docker container and executing notebooks. The easiest way to manually run/develop the notebooks is attaching to the docker container via VS Code.

---

## Step 1 - Build Container

Build & run docker container (you must have docker installed)

```
make docker_run
```

## Step 2 - Running within VS Code

- Open VS Code
- Open the Command Palette (F1)
    - Type `Dev Containers: Attach to Running Container`
    - Select the container
- In VS Code, open the `/code` folder from within the container.

You can now open and run all notebooks using VS Code or use the VS Code terminal to run commands e.g. from the Makefile.
