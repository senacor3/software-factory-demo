// @ts-check
// Separate, dedicated config for the `static_analysis` check (bug-pattern rules via
// eslint-plugin-sonarjs), independent of eslint.config.js (the existing style/formatting lint
// config `ng lint` runs). `ng lint` is pinned to one config via angular.json and can't swap
// configs per invocation, so this is invoked directly via `eslint -c
// eslint.static-analysis.config.js .` (see package.json's "static-analysis" script) rather than
// folded into the existing config or script.
const { defineConfig } = require('eslint/config');
const tseslint = require('typescript-eslint');
const sonarjs = require('eslint-plugin-sonarjs');

module.exports = defineConfig([
  {
    files: ['**/*.ts'],
    extends: [tseslint.configs.recommended, sonarjs.configs.recommended],
  },
]);
