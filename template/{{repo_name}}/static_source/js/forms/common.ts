declare global {
    interface Element {
        active: boolean;
    }
  }

function getInput(component: Element): HTMLInputElement | HTMLTextAreaElement | null {
  if (component.matches("input, textarea")) {
    return component as HTMLInputElement;
  } else if (component.querySelector("input, textarea")) {
    return component.querySelector("input, textarea") as HTMLInputElement;
  }
  return null;
}

function updateFlag(this: HTMLElement & { $el: Element }, e: Event) {
  const currentInput: HTMLInputElement | HTMLTextAreaElement | null = getInput(this.$el);

  if (!currentInput) {
    console.warn("alpine input attached to something that isn't an input");
    return;
  }

  switch (e.type) {
    case "focus":
    case "input":
      this.active = true;
      break;
    case "blur":
      if (!currentInput.value) {
        this.active = false;
      } else {
        this.active = true;
      }
      break;
    default:
  }

  if (currentInput.classList.contains("autofilled")) {
    currentInput.classList.remove("autofilled");
  }
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function inputListener(this:any) {
  const currentComponent = this.$el as HTMLInputElement;
  const currentInput = getInput(currentComponent);
  if (!currentInput) {
    return;
  }

  // Each of these events can have a different effect on the active state of the input.
  ["blur", "focus", "input"].forEach((eventName) => {
    currentInput.addEventListener(eventName, updateFlag.bind(this));
  });

  // We're using the animationstart event to detect when the browser has autofilled
  currentInput.addEventListener("animationstart", (e: Event) => {
    const { animationName } = e as AnimationEvent;
    if (!animationName) {
      return;
    }
    switch (animationName) {
      case "autofill-start":
        this.active = true;
        currentInput.classList.add("autofilled");
        break;
      case "autofill-cancel":
        if (document.activeElement === currentInput) {
          this.active = true;
        } else if (this.value === "") {
          this.active = false;
        }
        if (!currentInput.value) {
          currentInput.classList.remove("autofilled");
        }
        break;
      default:
    }
  });
}
