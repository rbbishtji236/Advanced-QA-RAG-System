import os
import pandas as pd
from typing import Tuple,Sequence
from pathlib import Path
from datetime import datetime, date
from zoneinfo import ZoneInfo

class Memory:

    @staticmethod
    def write_chat_history_to_file(
        gradio_chatbot: Sequence[Tuple[str, str]],
        thread_id: str,
        folder_path: str,
        tz: str = "Asia/Kolkata",
    ) -> None:
        if not gradio_chatbot:
            return

        last = gradio_chatbot[-1]
        if isinstance(last, dict):
            user = last.get("user") or last.get("user_query") or last.get("question") or ""
            bot = last.get("bot") or last.get("response") or last.get("answer") or ""
        else:
            last = list(last)
            user = last[0] if len(last) > 0 else ""
            bot = last[1] if len(last) > 1 else ""

        out_dir = Path(folder_path)
        out_dir.mkdir(parents=True, exist_ok=True)

        today_str = date.today().strftime("%Y-%m-%d")
        ts_str = datetime.now(ZoneInfo(tz)).strftime("%H:%M:%S")
        file_path = out_dir / f"{today_str}.csv"


        row = pd.DataFrame([[thread_id, ts_str, user, bot]],
                           columns=["thread_id", "timestamp", "user_query", "response"])


        write_header = not file_path.exists()
        row.to_csv(file_path, mode="a", header=write_header, index=False, encoding="utf-8")
