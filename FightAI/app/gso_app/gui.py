"""Tkinter-based GUI for running grappling skeleton analysis."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from tkinter import BooleanVar, StringVar, Tk, messagebox
from tkinter import filedialog, ttk

from gso_app.cli import analyze_video
from gso_app.paths import resolve_config_path


DEFAULT_CONFIG_PATH = resolve_config_path()


@dataclass
class GuiSettings:
    input_path: str = ""
    output_dir: str = str(Path.cwd() / "artifacts")
    write_summary: bool = True
    write_metrics: bool = True
    write_analysis: bool = True

    @classmethod
    def from_payload(cls, payload: dict) -> "GuiSettings":
        return cls(
            input_path=payload.get("input_path", ""),
            output_dir=payload.get("output_dir", str(Path.cwd() / "artifacts")),
            write_summary=payload.get("write_summary", True),
            write_metrics=payload.get("write_metrics", True),
            write_analysis=payload.get("write_analysis", True),
        )


def load_settings(config_path: Path) -> GuiSettings:
    if config_path.exists():
        payload = json.loads(config_path.read_text(encoding="utf-8"))
        return GuiSettings.from_payload(payload)
    return GuiSettings()


def save_settings(config_path: Path, settings: GuiSettings) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(asdict(settings), indent=2) + "\n",
        encoding="utf-8",
    )


class GuiApp:
    def __init__(self, root: Tk, config_path: Path) -> None:
        self.root = root
        self.config_path = config_path
        self.settings = load_settings(config_path)

        self.input_path = StringVar(value=self.settings.input_path)
        self.output_dir = StringVar(value=self.settings.output_dir)
        self.write_summary = BooleanVar(value=self.settings.write_summary)
        self.write_metrics = BooleanVar(value=self.settings.write_metrics)
        self.write_analysis = BooleanVar(value=self.settings.write_analysis)
        self.status = StringVar(value="Ready")

        self._build_layout()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_layout(self) -> None:
        self.root.title("GSO Analyzer")
        main = ttk.Frame(self.root, padding=16)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(main, text="Input video").grid(row=0, column=0, sticky="w")
        input_entry = ttk.Entry(main, textvariable=self.input_path, width=60)
        input_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(main, text="Browse", command=self._browse_input).grid(
            row=1, column=1, sticky="ew"
        )

        ttk.Label(main, text="Output directory").grid(row=2, column=0, sticky="w", pady=(12, 0))
        output_entry = ttk.Entry(main, textvariable=self.output_dir, width=60)
        output_entry.grid(row=3, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(main, text="Browse", command=self._browse_output).grid(
            row=3, column=1, sticky="ew"
        )

        options_frame = ttk.LabelFrame(main, text="Artifacts", padding=12)
        options_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(16, 0))
        options_frame.columnconfigure(0, weight=1)

        ttk.Checkbutton(
            options_frame,
            text="Write summary.txt",
            variable=self.write_summary,
        ).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(
            options_frame,
            text="Write metrics.json",
            variable=self.write_metrics,
        ).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(
            options_frame,
            text="Write analysis.json",
            variable=self.write_analysis,
        ).grid(row=2, column=0, sticky="w")

        action_frame = ttk.Frame(main)
        action_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(16, 0))
        action_frame.columnconfigure(0, weight=1)

        ttk.Button(action_frame, text="Run / Generate", command=self._run).grid(
            row=0, column=0, sticky="e"
        )
        ttk.Label(main, textvariable=self.status).grid(row=6, column=0, columnspan=2, sticky="w")

        main.columnconfigure(0, weight=1)

    def _browse_input(self) -> None:
        path = filedialog.askopenfilename(title="Select input video")
        if path:
            self.input_path.set(path)

    def _browse_output(self) -> None:
        path = filedialog.askdirectory(title="Select output directory")
        if path:
            self.output_dir.set(path)

    def _run(self) -> None:
        input_value = self.input_path.get().strip()
        output_value = self.output_dir.get().strip()
        input_path = Path(input_value).expanduser()
        output_dir = Path(output_value).expanduser()

        if not input_value or not input_path.exists():
            messagebox.showerror("Invalid input", "Input video path does not exist.")
            return
        if not output_value:
            messagebox.showerror("Invalid output", "Output directory is required.")
            return

        self.status.set("Running analysis...")
        self.root.update_idletasks()

        analyze_video(
            input_path=input_path,
            output_dir=output_dir,
            write_summary=self.write_summary.get(),
            write_metrics=self.write_metrics.get(),
            write_analysis=self.write_analysis.get(),
        )

        self.settings = GuiSettings(
            input_path=str(input_path),
            output_dir=str(output_dir),
            write_summary=self.write_summary.get(),
            write_metrics=self.write_metrics.get(),
            write_analysis=self.write_analysis.get(),
        )
        save_settings(self.config_path, self.settings)
        self.status.set("Complete. Artifacts written.")

    def _on_close(self) -> None:
        self.settings = GuiSettings(
            input_path=self.input_path.get(),
            output_dir=self.output_dir.get(),
            write_summary=self.write_summary.get(),
            write_metrics=self.write_metrics.get(),
            write_analysis=self.write_analysis.get(),
        )
        save_settings(self.config_path, self.settings)
        self.root.destroy()


def launch_gui(config_path: Path | None = None) -> int:
    resolved_path = config_path or DEFAULT_CONFIG_PATH
    root = Tk()
    GuiApp(root, resolved_path)
    root.mainloop()
    return 0
