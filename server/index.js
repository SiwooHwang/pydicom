import serverConfig from "./config.js";
import express from "./express.js";

const PORT = serverConfig.port;
const HOST = serverConfig.host;

async function startServer() {
  const app = express.init();

  app.listen(PORT, HOST, () => {
    logger.info(`Example app listening on port http://${HOST}:${PORT}`);
  });
}

process.on("uncaughtException", (err) => {
  logger.error("uncaughtException err -", err.stack);
  process.exit(1);
});

process.on("unhandledRejection", (err, promise) => {
  logger.error("unhandledRejection promise -", promise);
  logger.error("unhandledRejection err -", err);
});

startServer();
