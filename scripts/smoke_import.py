"""Smoke test for the production WSGI entrypoint."""

import importlib


def main():
    module = importlib.import_module("app")
    if not hasattr(module, "server"):
        raise RuntimeError("app module does not expose the expected WSGI server")
    print("app:server import ok")


if __name__ == "__main__":
    main()
