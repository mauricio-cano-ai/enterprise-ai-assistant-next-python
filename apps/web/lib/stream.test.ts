import { describe, expect, it, vi } from "vitest";
import { parseNdjsonStream } from "./stream";

function streamOf(...parts: string[]) {
  const encoder = new TextEncoder();
  return new ReadableStream<Uint8Array>({
    start(controller) {
      parts.forEach((part) => controller.enqueue(encoder.encode(part)));
      controller.close();
    },
  });
}

describe("parseNdjsonStream", () => {
  it("handles JSON lines split across network chunks", async () => {
    const onEvent = vi.fn();
    await parseNdjsonStream(
      streamOf('{"type":"token","text":"Hel', 'lo"}\n{"type":"done"}\n'),
      onEvent,
    );

    expect(onEvent).toHaveBeenNthCalledWith(1, { type: "token", text: "Hello" });
    expect(onEvent).toHaveBeenNthCalledWith(2, { type: "done" });
  });
});
