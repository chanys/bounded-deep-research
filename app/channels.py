"""Channel registry: the corpora the app can serve.

One entry per ingested YouTube channel. This is the single source of truth for
per-channel behavior: the UI fetches it via GET /channels (display name + example
prompts), POST /query validates the requested channel against it, and the agent
appends `output_directive` (when set) to the system prompt so the answer comes
out in the channel's language without forking the research recipe.
"""

from pydantic import BaseModel


class Channel(BaseModel):
    id: str                      # the `videos.channel` value in the DB (the YouTube handle)
    display_name: str            # what the UI shows (the channel's display name, not the handle)
    language: str                # language of the transcripts and the answer ("en" | "zh")
    example_prompts: list[str]   # the one-click example cards under the ask box
    # Appended to the system prompt for this channel. None = recipe as-is (English).
    output_directive: str | None = None


# Insertion order is the display order in the UI picker; the first entry is the default.
CHANNELS: dict[str, Channel] = {
    c.id: c
    for c in [
        Channel(
            id="TransGlobalTV",
            display_name="TransGlobal TV (泛宇財經頻道)",
            language="zh",
            example_prompts=[
                "頻道如何比較年金與人壽保險在退休規劃中的角色？",
                "頻道對聯準會降息的看法在2025到2026年間有何變化？",
            ],
            output_directive=(
                "The transcripts in this corpus are in Traditional Chinese. Phrase your "
                "`search_transcripts` queries in Chinese to match the corpus. Write the final "
                "answer and every citation `reason` in Traditional Chinese (繁體中文)."
            ),
        ),
        Channel(
            id="code4AI",
            display_name="Discover AI",
            language="en",
            example_prompts=[
                "How does the creator distinguish RAG from the broader 'AI harness', and what role does each play?",
                "How has the creator's view of LLM reasoning evolved over 2025-2026?",
            ],
        ),
    ]
}
