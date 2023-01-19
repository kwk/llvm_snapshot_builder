# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

## Types of Contributions

### Report Bugs

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

You can never have enough documentation! Please feel free to contribute to any
part of the documentation, such as the official docs, docstrings, or even
on the web in blog posts, articles, and such.

### Submit Feedback

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `llvm_snapshot_builder` for local development.

1. Download the sources:

     ```console
     $ git clone git@github.com:kwk/llvm_snapshot_builder.git
     ```

2. Enter the source directory:

     ```console
     $ cd llvm_snapshot_builder
     ```
3. Create a virtual environment using:

     ```console
     $ poetry shell`
     ```

4. Install the sources into the virtual environment that you're in:

     ```console
     $ poetry install
     ```

5. Try out the CLI tool:

     ```console
     $ llvm_sb
     ```

   You should see some help showing up there.

6. Use `git` (or similar) to create a branch for local development and make your changes:

    ```console
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

7. When you're done making changes, check that your changes conform to any code formatting requirements and pass any tests.

8. Commit your changes and open a pull request.

## Run tests

After you've completed steps 1-4 from the previous steps you need to setup your
Copr credentials by going to https://copr.fedorainfracloud.org/api/ and then
creating a `~/.config/copr` file according to the information on the website.
This project will automatically pick up the config from that file in order to
connect you to copr and create test projects for you in there when you run tests.

Run all tests by executing:

    ```console
    $ poetry run pytest
    ```

In order to run an intivial test, try this:

    ```console
    pytest tests/test_cli.py::TestCLI::test_project_exists
    ```

And adjust the path to the test you want to run.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include additional tests if appropriate.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for all currently supported operating systems and versions of Python.

## Code of Conduct

Please note that the `llvm_snapshot_builder` project is released with a
Code of Conduct. By contributing to this project you agree to abide by its terms.
