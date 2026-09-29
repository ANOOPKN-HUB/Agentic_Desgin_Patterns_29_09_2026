"""Forward the legacy singular module path to ``patterns.tools_using.run``."""

import runpy


if __name__ == "__main__":
    runpy.run_module("patterns.tools_using.run", run_name="__main__")