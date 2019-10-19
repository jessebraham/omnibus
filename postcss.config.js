const autoprefixer  = require("autoprefixer");
const cssnano       = require("cssnano");
const postcssimport = require("postcss-import");
const purgecss      = require("@fullhuman/postcss-purgecss");
const tailwindcss   = require("tailwindcss");

// Constant flag to indicate whether or not we should build for production.
const PRODUCTION = process.env.NODE_ENV === "production";

// Custom PurgeCSS extractor for Tailwind that allows special characters in
// class names.
//
// https://github.com/FullHuman/purgecss#extractor
class TailwindExtractor {
  static extract(content) {
    return content.match(/[A-Za-z0-9-_:\/]+/g) || [];
  }
}

module.exports = ctx => ({
  map:    ctx.options.map,
  parser: ctx.options.parser,

  plugins: [
    autoprefixer,
    postcssimport,
    tailwindcss,

    // Production mode only
    PRODUCTION && purgecss({
      content: [
        "./web/templates/**/*.html",
        "./web/templates/**/*.jinja",
        "./web/static/js/**/*.js",
      ],
      css: ["./web/static/css/**/*.css"],
      extractors: [
        {
          extractor: TailwindExtractor,
          extensions: ["html", "css", "js", "jinja"],
        },
      ],
      whitelist: [],
      whitelistPatternsChildren: [],
    }),
    PRODUCTION && cssnano({
      preset: "default",
    }),
  ],
});
