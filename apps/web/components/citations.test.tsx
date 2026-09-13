import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";
import { Citations } from "./citations";

it("renders citation-safe metadata", () => {
  render(
    <Citations
      citations={[
        {
          id: "eval-guide",
          title: "AI Evaluation Guide",
          snippet: "Use a golden dataset.",
          section: "Regression gates",
        },
      ]}
    />,
  );

  expect(screen.getByText("AI Evaluation Guide")).toBeInTheDocument();
  expect(screen.getByText(/Regression gates/)).toBeInTheDocument();
  expect(screen.getByText(/Use a golden dataset/)).toBeInTheDocument();
});
