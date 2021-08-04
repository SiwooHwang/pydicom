import express from "express";
import cors from "cors";
import router from "./routes";
import serverConfig from "./config";

export default {
  init() {
    const app = express();

    app.use(cors({ origin: serverConfig.corsOrigin, credentials: true }));
    app.use("/", router);

    return app;
  },
};
