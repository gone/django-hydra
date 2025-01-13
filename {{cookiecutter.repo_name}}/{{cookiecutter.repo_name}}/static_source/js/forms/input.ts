import AlpineInstance, { AlpineComponent } from "alpinejs";
import inputListener from "./common";

interface Input {
  //callback requires indexing to string and symbol
  [key: string]: unknown;
  [key: symbol]: unknown;
  //real types
  eventName: string;
  value: string;
  type: string;
  active: boolean;
}


const input = (...args: unknown[]): AlpineComponent<Input> => {
  const [eventName, value, type] = args as [string, string, string];
  return {
    eventName,
    value,
    type,
    active: false,
    init() {
      inputListener.call(this);

      if (this.type === 'checkbox') {
        // For checkboxes, initial state can come from either value or checked attribute
        const input = this.$el as HTMLInputElement;
        this.value = (value === true || value === 'true' || value === 'on' || input.hasAttribute('checked')) ? 'on' : '';

        // Convert boolean true to 'on' for Django compatibility
        this.$watch('value', (newVal) => {
          if (newVal === true) {
            this.value = 'on';
          } else if (newVal === false) {
            this.value = '';
          }
        });
      } else if (this.value === "None") {
        this.value = "";
      } else if (this.$refs !== undefined && "input" in this.$refs) {
        // Toggle the focused state on an input when an initial value is set.
        this.active = !this.active;
      }
      if (this.eventName !== "input") {
        this.$watch("value", () => {
          this.$dispatch(
            this.eventName,
            { value: this.value },
          );
        });
      }
    },
  }
}
AlpineInstance.data("input", input);
