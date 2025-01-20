import { Alpine as AlpineType } from "alpinejs";

declare global {
  interface Window {
    Alpine: AlpineType;
  }
  const Alpine: AlpineType;
}
