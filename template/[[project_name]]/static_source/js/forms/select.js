import Alpine from "alpinejs";
import TomSelect from "tom-select";
import "tom-select/dist/css/tom-select.bootstrap5.css"; // doesn't actually include bootstrap, easy to style

const select = () => ({
  init() {
    // give a timeout to let htmx finish swapping content in
    // eslint-disable-next-line  no-undef
    setTimeout(() => {
      const control = this.$el;

      new TomSelect(control, {
      });
    }, 80);
  },
});

Alpine.data("select", select);
