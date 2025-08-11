
import csv
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import gradio as gr

TZ = ZoneInfo("Asia/Kolkata")

@dataclass
class FeedbackRecord:
    timestamp: str
    thread_id: str
    liked: bool
    value: str

class UISettings:
    """
    Utility class for managing UI settings and feedback capture.
    """
    @staticmethod
    def feedback(data: gr.LikeData, thread_id: str = "default", out_dir: str = "data/feedback") -> None:
        """
        Store user feedback (like/dislike) for a generated response.

        Args:
            data: Gradio LikeData with fields .liked (bool) and .value (str)
            thread_id: your chat/session id (pass via gr.State)
            out_dir: folder to store daily CSVs
        """
        ts = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
        rec = FeedbackRecord(timestamp=ts, thread_id=thread_id, liked=bool(data.liked), value=data.value or "")

        out_path = Path(out_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        csv_path = out_path / f"{ts[:10]}.csv"

        write_header = not csv_path.exists()
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(asdict(rec).keys()))
            if write_header:
                w.writeheader()
            w.writerow(asdict(rec))

        print(("Upvoted" if rec.liked else "Downvoted") + f": {rec.value[:120]}")
