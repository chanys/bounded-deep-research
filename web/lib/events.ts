// TypeScript mirror of app/events.py — the SSE event contract.
// Keep these in lockstep with the backend Pydantic models. The discriminated
// union (switch on `type`) is what lets the UI handle each event safely and
// lets TypeScript narrow the shape inside each branch.

export type TokenUsage = {
  input_tokens: number;
  cached_input_tokens: number; // subset of input_tokens, billed cheaper
  output_tokens: number; // includes reasoning_tokens
  reasoning_tokens: number;
  total_tokens: number;
};

export type RunStarted = {
  type: "run_started";
  run_id: string; // key for GET /runs/{run_id}/evidence
  query: string;
  channel: string;
  mode: string;
  recipe_version: string;
};

export type TurnStart = {
  type: "turn_start";
  step: number;
};

export type TurnComplete = {
  type: "turn_complete";
  step: number;
  usage: TokenUsage;
};

export type SearchStart = {
  type: "search_start";
  search_id: number;
  query: string;
  mode: string;
};

export type SearchComplete = {
  type: "search_complete";
  search_id: number;
  result_count: number;
  returned_chunk_ids: string[];
};

export type ReadStart = {
  type: "read_start";
  read_id: number;
  video_id: string;
  start_ts: number;
};

export type ReadComplete = {
  type: "read_complete";
  read_id: number;
  ok: boolean; // false if the chunk wasn't found
  chunk_id?: string;
  video_id?: string;
  start_ts?: number;
  end_ts?: number;
};

export type Citation = {
  video_id: string;
  start_ts: number;
  end_ts: number;
};

export type AnswerComplete = {
  type: "answer_complete";
  answer: string;
  citations: Citation[];
};

export type ErrorEvent = {
  type: "error";
  message: string;
};

// The full set of events that can arrive on the /query stream.
export type SseEvent =
  | RunStarted
  | TurnStart
  | TurnComplete
  | SearchStart
  | SearchComplete
  | ReadStart
  | ReadComplete
  | AnswerComplete
  | ErrorEvent;
