from __future__ import annotations

import sys


def main(argv: list[str]) -> int:
    if "--cli" in argv:
        from cli import main as cli_main

        return cli_main([argv[0]] + [a for a in argv[1:] if a != "--cli"])

    try:
        from app import main as app_main
    except ImportError:
        print(
            "pywebview não está instalado. Instale com 'pip install -r requirements.txt'\n"
            "ou rode a versão em terminal: python main.py --cli",
            file=sys.stderr,
        )
        return 1

    app_main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
