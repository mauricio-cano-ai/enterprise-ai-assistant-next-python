export type Citation = {
  id: string;
  title: string;
  snippet: string;
  source_url?: string | null;
  section?: string | null;
};

export type ChatStreamEvent =
  | { type: "token"; text: string }
  | { type: "citation"; citation: Citation }
  | { type: "error"; message: string }
  | { type: "done" };
