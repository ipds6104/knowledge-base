"""adapters/vision_toptools.py — Top Tools AI Vision Adapter implementing VisionClientPort.

Tanggung Jawab Tunggal:
Mengelola komunikasi HTTP dengan Top Tools AI Vision API (OpenAI-compatible)
untuk mentranskripsikan gambar slide menjadi teks Markdown terstruktur.
"""

import json
import time
import urllib.error
import urllib.request

from ..domain import SLIDE_SYSTEM_PROMPT_TEMPLATE
from ..ports import VisionClientPort


class TopToolsVisionAdapter(VisionClientPort):
    """Adapter untuk berkomunikasi dengan Top Tools AI multimodal vision endpoint."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://top-tools-ai.com/api/v1",
        model: str = "Top-Tools-Ai",
        timeout: int = 60,
        max_retries: int = 3,
    ):
        if not api_key:
            raise ValueError("API Key Top Tools AI wajib disediakan.")
        self.api_key = api_key
        # Pastikan URL mengarah ke endpoint chat completions
        clean_base = base_url.rstrip("/")
        if not clean_base.endswith("/chat/completions"):
            self.endpoint_url = f"{clean_base}/chat/completions"
        else:
            self.endpoint_url = clean_base

        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries

    def transcribe_slide(
        self,
        image_base64: str,
        slide_number: int,
        total_slides: int,
    ) -> str:
        """Mengirim gambar slide ke model vision Top Tools AI dan mengembalikan teks Markdown."""
        system_prompt = SLIDE_SYSTEM_PROMPT_TEMPLATE.format(
            slide_number=slide_number,
            total_slides=total_slides,
        )

        user_instruction = (
            f"Analisis dan transkripsikan seluruh isi slide {slide_number} "
            f"ini ke dalam format Markdown komprehensif sesuai aturan sistem:"
        )

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_instruction},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            },
                        },
                    ],
                },
            ],
            "temperature": 0.15,
        }

        req_body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            req = urllib.request.Request(
                self.endpoint_url,
                data=req_body,
                headers=headers,
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    choices = resp_data.get("choices", [])
                    if not choices:
                        raise RuntimeError("Respons API tidak memuat choices output.")
                    return choices[0]["message"]["content"].strip()
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
                last_error = e
                # Jika rate-limit 429 atau server error 5xx, tunggu sejenak sebelum retry
                if attempt < self.max_retries:
                    backoff = attempt * 2
                    time.sleep(backoff)

        raise RuntimeError(
            f"Gagal memproses slide {slide_number} setelah {self.max_retries} percobaan: {last_error}"
        )
