const input = document.querySelector("#content");
const counter = document.querySelector("#char-count");
const clearButton = document.querySelector("#clear-content");

if (input && counter) {
  const updateCounter = () => {
    counter.textContent = `${input.value.length.toLocaleString("pt-BR")} / 1.000`;
  };
  input.addEventListener("input", updateCounter);
  updateCounter();

  document.querySelectorAll("[data-sample]").forEach((button) => {
    button.addEventListener("click", () => {
      input.value = button.dataset.sample;
      updateCounter();
      const motion = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
      document.querySelector("#analisar").scrollIntoView({ behavior: motion, block: "center" });
      input.focus({ preventScroll: true });
    });
  });

  clearButton?.addEventListener("click", () => {
    input.value = "";
    updateCounter();
    input.focus();
  });
}

const result = document.querySelector("#resultado");
if (result) {
  result.scrollIntoView({ behavior: "auto", block: "start" });
}

