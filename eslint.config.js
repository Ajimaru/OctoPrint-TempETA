const globals = require("globals");

module.exports = [
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "script",
      globals: {
        ...globals.es2021,
        ...globals.browser,
        ...globals.node,
        $: "readonly",
        ko: "readonly",
        OctoPrint: "readonly",
        PNotify: "readonly",
        gettext: "readonly",
        OCTOPRINT_VIEWMODELS: "readonly",
      },
    },
    rules: {},
  },
];
