import AlpineInstance, { AlpineComponent } from "alpinejs";
import flatpickr from "flatpickr";

import "flatpickr/dist/themes/light.css";
import inputListener from "./common";

interface DateTime{
  //callback requires indexing to string and symbol
  [key: string]: unknown;
  [key: symbol]: unknown;
  //real types
  eventName: string;
  value: string;
  enableTime: boolean;
  picker: flatpickr.Instance | null;
}


const dateTime = (...args: unknown[]): AlpineComponent<DateTime> => {
  const [eventName, value, enableTime] = args as [string, string, boolean];
  return {
    eventName,
    value,
    enableTime,
    picker: null,
    active: false,
    init() {
      inputListener.call(this);

      if (this.value === "None") {
        this.value = "";
      }

      // see https://flatpickr.js.org/formatting/
      const dateFormat = enableTime ? "m/d/Y H:i" : "m/d/Y";

      this.picker = flatpickr(this.$refs.picker, {
        mode: "single",
        enableTime,
        dateFormat,
        defaultDate: value,
        onChange: (_, dateString) => {
          this.value = dateString;
        },
      });

      this.$watch("value", () => {
        this.picker?.setDate(this.value);
        if (this.eventName !== "") this.$dispatch(this.eventName, { value: this.value });
      });

      if (this.value) {
        this.active = true;
      }
    },
  }
};

AlpineInstance.data("dateTime", dateTime);
