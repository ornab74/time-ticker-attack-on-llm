import argparse
import csv
import json
import math
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEPS = Path(__file__).with_name(".deps")
if DEPS.exists():
    sys.path.insert(0, str(DEPS))

import customtkinter as ctk

DISCLAIMER = (
    "SYNTHETIC HYPOTHESIS — NOT EVIDENCE OF A REAL BREACH, MODEL, DATASET, "
    "OR ORGANIZATION. ALL EVENTS AND SCORES ARE FICTIONAL."
)

BG = "#060914"
PANEL = "#101629"
EDGE = "#263354"
TEXT = "#EDF4FF"
MUTED = "#8291B5"
CYAN = "#34D6FF"
PURPLE = "#A977FF"
ORANGE = "#FFAA4C"
RED = "#FF5F79"
GREEN = "#46E69A"

STAGES = [
    ("SOURCE", CYAN, "Synthetic media enters an imagined corpus"),
    ("ENCODE", PURPLE, "Abstract hidden-pattern signal is introduced"),
    ("INGEST", ORANGE, "Fictional curation pipeline accepts samples"),
    ("TRAIN", RED, "Toy learner develops a measurable correlation"),
    ("RECALL", GREEN, "Canary-style probe detects simulated influence"),
]


def generate_records(seed=7429, count=240):
    rng = random.Random(seed)
    start = datetime(2019, 1, 1, tzinfo=timezone.utc)
    records = []
    for i in range(count):
        stage_idx = min(4, i // 48)
        stage, _, _ = STAGES[stage_idx]
        age = i / (count - 1)
        hidden_signal = max(0.0, min(1.0, 0.08 + 0.66 * age + rng.gauss(0, 0.07)))
        contamination = max(0.0, min(1.0, hidden_signal * (0.22 + stage_idx * 0.13)))
        memorization = max(0.0, min(1.0, contamination ** 1.35 + rng.gauss(0, 0.025)))
        detection = max(0.0, min(1.0, 0.12 + memorization * 0.79 + rng.gauss(0, 0.04)))
        records.append({
            "record_id": f"SYN-{i + 1:04d}",
            "timestamp": (start + timedelta(days=i * 9)).isoformat(),
            "stage": stage,
            "hidden_signal_score": round(hidden_signal, 4),
            "simulated_contamination_score": round(contamination, 4),
            "toy_memorization_score": round(memorization, 4),
            "canary_detection_score": round(detection, 4),
            "ground_truth": "synthetic_positive" if i % 7 in (0, 1) else "synthetic_control",
            "evidence_status": "FICTIONAL_SIMULATION_ONLY",
        })
    return records


def write_outputs(directory):
    directory.mkdir(parents=True, exist_ok=True)
    records = generate_records()
    json_path = directory / "synthetic_training_leak_simulation.json"
    csv_path = directory / "synthetic_training_leak_simulation.csv"
    report_path = directory / "hypothetical_incident_report.md"

    json_path.write_text(json.dumps({
        "disclaimer": DISCLAIMER,
        "seed": 7429,
        "model": "toy_world_model_v1",
        "records": records,
    }, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    positives = [r for r in records if r["ground_truth"] == "synthetic_positive"]
    controls = [r for r in records if r["ground_truth"] == "synthetic_control"]
    p_mean = sum(r["canary_detection_score"] for r in positives) / len(positives)
    c_mean = sum(r["canary_detection_score"] for r in controls) / len(controls)
    peak = max(r["toy_memorization_score"] for r in records)

    report_path.write_text(f"""# Hypothetical Training-Data Influence Simulation

> **{DISCLAIMER}**

## Executive summary

This project simulates an imagined path in which a hidden statistical pattern is introduced into synthetic media, passes through a fictional ingestion pipeline, influences a toy learner, and is later detected with canary-style probes. The generated records are demonstration data. They do **not** show that Hugging Face, a real model, or any real training dataset was attacked, accessed, poisoned, or leaked.

## Synthetic result

- Records: **{len(records)}**
- Fixed simulation seed: **7429**
- Mean fictional canary score, synthetic-positive group: **{p_mean:.3f}**
- Mean fictional canary score, control group: **{c_mean:.3f}**
- Peak toy memorization score: **{peak:.3f}**
- Evidentiary value for real-world claims: **none**

The simulator deliberately creates increasing correlations, so elevated scores are an expected consequence of its equations—not an independently discovered fact. It models a proposition; it does not verify that proposition.

## Hypothetical pathway

1. **Source:** synthetic media is added to an imagined corpus.
2. **Encode:** an abstract hidden-pattern score is assigned. No operational steganographic payload is produced.
3. **Ingest:** a fictional filter accepts the synthetic samples.
4. **Train:** a toy memorization score increases as a mathematical function of simulated contamination.
5. **Recall:** canary-style probes report higher scores where the simulator planted stronger influence.

## What real evidence would require

A credible investigation would need authenticated dataset provenance, immutable hashes, signed ingestion logs, model/version identifiers, reproducible black-box or white-box tests, statistically valid controls, an independently reviewed chain of custody, and confirmation from the affected maintainers. Similar outputs, surprising model behavior, or this simulation alone cannot establish poisoning, data leakage, unauthorized access, or causation.

## Defensive interpretation

The useful lesson is methodological: retain provenance records, scan training assets for anomalous structure, deduplicate across modalities, isolate untrusted model artifacts, restrict execution permissions, use signed artifacts, test canaries against matched controls, and require independent reproduction before escalating a hypothesis into an incident claim.
""", encoding="utf-8")
    return json_path, csv_path, report_path


class WorldModelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hypothetical World Model Visualizer")
        self.geometry("1180x720")
        self.configure(fg_color=BG)
        self.resizable(False, False)

        ctk.CTkLabel(
            self, text="WORLD MODEL // HYPOTHETICAL INCIDENT MIND",
            text_color=TEXT, font=ctk.CTkFont(size=25, weight="bold")
        ).place(x=34, y=26)
        ctk.CTkLabel(
            self, text="SYNTHETIC SIMULATION — NOT REAL-WORLD EVIDENCE",
            text_color=ORANGE, font=ctk.CTkFont(size=12, weight="bold")
        ).place(x=36, y=63)

        canvas_panel = ctk.CTkFrame(
            self, width=1112, height=395, fg_color=PANEL,
            border_width=1, border_color=EDGE, corner_radius=20
        )
        canvas_panel.place(x=34, y=99)
        self.canvas = ctk.CTkCanvas(
            canvas_panel, width=1070, height=350, bg=PANEL,
            highlightthickness=0
        )
        self.canvas.place(x=20, y=20)
        self.draw_world()

        cards = [
            ("240", "SYNTHETIC RECORDS", CYAN),
            ("0.742", "PEAK TOY INFLUENCE", PURPLE),
            ("5", "FICTIONAL STAGES", ORANGE),
            ("ZERO", "REAL EVIDENCE", GREEN),
        ]
        for i, (value, label, color) in enumerate(cards):
            x = 34 + i * 280
            card = ctk.CTkFrame(
                self, width=262, height=104, fg_color=PANEL,
                border_width=1, border_color=EDGE, corner_radius=16
            )
            card.place(x=x, y=516)
            ctk.CTkLabel(
                card, text=value, text_color=color,
                font=ctk.CTkFont(size=29, weight="bold")
            ).place(x=20, y=14)
            ctk.CTkLabel(
                card, text=label, text_color=MUTED,
                font=ctk.CTkFont(size=11, weight="bold")
            ).place(x=20, y=64)

        ctk.CTkLabel(
            self,
            text="This visualization plants its own signal. It cannot prove a historical attack.",
            text_color=MUTED, font=ctk.CTkFont(size=14)
        ).place(x=36, y=658)
        ctk.CTkButton(
            self, text="EXPORT SYNTHETIC DATA", width=220, height=42,
            corner_radius=12, fg_color=PURPLE, hover_color="#8A55DD",
            command=lambda: write_outputs(Path.cwd())
        ).place(x=926, y=647)

    def draw_world(self):
        xs = [95, 315, 535, 755, 975]
        center_y = 155
        for i in range(4):
            self.canvas.create_line(
                xs[i] + 67, center_y, xs[i + 1] - 67, center_y,
                fill="#33466D", width=4, arrow="last"
            )
        for i, (name, color, desc) in enumerate(STAGES):
            x = xs[i]
            for radius, shade in ((65, "#17223A"), (48, "#1B2945")):
                self.canvas.create_oval(
                    x - radius, center_y - radius, x + radius, center_y + radius,
                    fill=shade, outline=color if radius == 65 else shade,
                    width=2
                )
            self.canvas.create_text(
                x, center_y - 4, text=name, fill=color,
                font=("DejaVu Sans", 13, "bold")
            )
            self.canvas.create_text(
                x, 255, text=desc, fill=MUTED,
                width=175, font=("DejaVu Sans", 10), justify="center"
            )
            angle = i * 0.9
            for j in range(6):
                a = angle + j * math.pi / 3
                px = x + math.cos(a) * 78
                py = center_y + math.sin(a) * 78
                self.canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill=color, outline="")


def make_screenshot(path):
    from PIL import Image, ImageDraw, ImageFont

    image = Image.new("RGB", (1180, 720), BG)
    draw = ImageDraw.Draw(image)

    def font(size, bold=False):
        suffix = "Bold" if bold else ""
        p = f"/usr/share/fonts/truetype/dejavu/DejaVuSans{('-' + suffix) if suffix else ''}.ttf"
        return ImageFont.truetype(p, size)

    draw.text((34, 24), "WORLD MODEL // HYPOTHETICAL INCIDENT MIND", fill=TEXT, font=font(25, True))
    draw.text((36, 62), "SYNTHETIC SIMULATION — NOT REAL-WORLD EVIDENCE", fill=ORANGE, font=font(12, True))
    draw.rounded_rectangle((34, 99, 1146, 494), radius=20, fill=PANEL, outline=EDGE)

    xs = [129, 349, 569, 789, 1009]
    cy = 274
    for i in range(4):
        draw.line((xs[i] + 66, cy, xs[i + 1] - 66, cy), fill="#33466D", width=4)
        draw.polygon([(xs[i + 1] - 69, cy - 7), (xs[i + 1] - 55, cy), (xs[i + 1] - 69, cy + 7)], fill="#33466D")
    for i, (name, color, desc) in enumerate(STAGES):
        x = xs[i]
        draw.ellipse((x - 65, cy - 65, x + 65, cy + 65), fill="#17223A", outline=color, width=2)
        draw.ellipse((x - 48, cy - 48, x + 48, cy + 48), fill="#1B2945")
        box = draw.textbbox((0, 0), name, font=font(13, True))
        draw.text((x - (box[2] - box[0]) / 2, cy - 9), name, fill=color, font=font(13, True))
        words = desc.split()
        lines, current = [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if draw.textlength(trial, font=font(10)) > 165:
                lines.append(current)
                current = word
            else:
                current = trial
        lines.append(current)
        for k, line in enumerate(lines):
            w = draw.textlength(line, font=font(10))
            draw.text((x - w / 2, 372 + k * 15), line, fill=MUTED, font=font(10))

    cards = [
        ("240", "SYNTHETIC RECORDS", CYAN),
        ("0.742", "PEAK TOY INFLUENCE", PURPLE),
        ("5", "FICTIONAL STAGES", ORANGE),
        ("ZERO", "REAL EVIDENCE", GREEN),
    ]
    for i, (value, label, color) in enumerate(cards):
        x = 34 + i * 280
        draw.rounded_rectangle((x, 516, x + 262, 620), radius=16, fill=PANEL, outline=EDGE)
        draw.text((x + 20, 529), value, fill=color, font=font(29, True))
        draw.text((x + 20, 580), label, fill=MUTED, font=font(11, True))
    draw.text(
        (36, 659),
        "This visualization plants its own signal. It cannot prove a historical attack.",
        fill=MUTED, font=font(14)
    )
    draw.rounded_rectangle((926, 647, 1146, 689), radius=12, fill=PURPLE)
    draw.text((948, 661), "EXPORT SYNTHETIC DATA", fill="#0B0712", font=font(12, True))
    image.save(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--screenshot")
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()
    if args.generate:
        write_outputs(Path(args.output_dir))
    if args.screenshot:
        make_screenshot(args.screenshot)
    if not args.generate and not args.screenshot:
        ctk.set_appearance_mode("dark")
        WorldModelApp().mainloop()
