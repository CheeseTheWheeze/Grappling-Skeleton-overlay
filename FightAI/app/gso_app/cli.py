import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from gso_app import installer
from gso_app.gui import launch_gui


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a grappling video and write analysis artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a video and produce output artifacts.",
    )
    analyze_parser.add_argument(
        "--input",
        required=True,
        help="Path to the input video file.",
    )
    analyze_parser.add_argument(
        "--output",
        required=True,
        help="Directory to write analysis artifacts.",
    )

    install_parser = subparsers.add_parser(
        "install",
        help="Verify prerequisites and initialize local assets.",
    )
    install_parser.add_argument(
        "--requirements",
        type=Path,
        default=installer.DEFAULT_REQUIREMENTS_PATH,
        help="Path to requirements.txt to install.",
    )
    install_parser.add_argument(
        "--config-dir",
        type=Path,
        default=installer.DEFAULT_CONFIG_DIR,
        help="Directory for configuration assets.",
    )

    gui_parser = subparsers.add_parser(
        "gui",
        help="Launch the GUI for configuring and running analysis.",
    )
    gui_parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the GUI configuration file.",
    )
    return parser


def analyze_video(
    input_path: Path,
    output_dir: Path,
    *,
    write_summary: bool = True,
    write_metrics: bool = True,
    write_analysis: bool = True,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, str] = {}
    if write_summary:
        artifacts["summary"] = str(output_dir / "summary.txt")
    if write_metrics:
        artifacts["metrics"] = str(output_dir / "metrics.json")
    if write_analysis:
        artifacts["analysis"] = str(output_dir / "analysis.json")

    analysis_payload = {
        "input": str(input_path),
        "status": "queued",
        "artifacts": artifacts,
    }

    if write_summary:
        (output_dir / "summary.txt").write_text(
            "Analysis placeholder. Replace with real model output.\n",
            encoding="utf-8",
        )
    if write_metrics:
        (output_dir / "metrics.json").write_text(
            json.dumps({"frames": 0, "detections": 0}, indent=2) + "\n",
            encoding="utf-8",
        )
    if write_analysis:
        (output_dir / "analysis.json").write_text(
            json.dumps(analysis_payload, indent=2) + "\n",
            encoding="utf-8",
        )


def run_install(requirements_path: Path, config_dir: Path) -> int:
    try:
        print("Checking Python version...")
        installer.verify_python_version()
        print("Installing/verifying requirements...")
        installer.install_requirements(requirements_path=requirements_path)
        print("Initializing assets/configuration...")
        final_config_dir = installer.initialize_assets(config_dir=config_dir)
        print("Creating desktop launcher...")
        desktop_entry = installer.create_desktop_launcher(
            config_dir=final_config_dir,
            requirements_path=requirements_path,
        )
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("Installation complete.")
    print(f"Configuration directory: {final_config_dir}")
    if desktop_entry:
        print(f"Desktop launcher created at: {desktop_entry}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        input_path = Path(args.input).expanduser().resolve()
        output_dir = Path(args.output).expanduser().resolve()
        if not input_path.exists():
            parser.error(f"Input video not found: {input_path}")
        analyze_video(input_path, output_dir)
        return 0

    if args.command == "install":
        requirements_path = Path(args.requirements).expanduser().resolve()
        config_dir = Path(args.config_dir).expanduser().resolve()
        return run_install(requirements_path, config_dir)

    if args.command == "gui":
        config_path = Path(args.config).expanduser().resolve() if args.config else None
        return launch_gui(config_path=config_path)

    parser.error("No command provided.")


if __name__ == "__main__":
    raise SystemExit(main())
