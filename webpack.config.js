const path                 = require("path");
const BundleTracker        = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin         = require("terser-webpack-plugin");

const { CleanWebpackPlugin } = require("clean-webpack-plugin");

// Constant flag to indicate whether or not we should build for production.
const PRODUCTION = process.env.NODE_ENV === "production";

module.exports = {
  entry: ["./web/static/css/main.css", "./web/static/js/index.js"],

  output: {
    path:     path.resolve("./web/static/dist/"),
    filename: "[name].[hash].js",
  },

  optimization: {
    minimize:  PRODUCTION,
    minimizer: PRODUCTION ? [new TerserPlugin()] : [],
  },

  module: {
    rules: [
      {
        test: /\.css$/,
        use:  [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader"],
      },
      {
        test:    /\.js$/,
        exclude: /node_modules/,
        use: [
          { loader: "babel-loader" },
          {
            loader: "prettier-loader",
            options: {
              parser: "babel",
              trailingComma: "all",
            },
          },
        ],
      },
    ],
  },

  plugins: [
    new BundleTracker({
      filename: "./webpack-stats.json",
    }),
    new CleanWebpackPlugin({
      cleanOnceBeforeBuildPatterns: ["**/*"],
    }),
    new MiniCssExtractPlugin({
      filename: "[name].[hash].css",
    }),
  ],
};
