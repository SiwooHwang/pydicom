import dotenv from "dotenv";
import path from "path";

dotenv.config();

export default {
  nodeEnv: process.env.NODE_ENV || "development",
  publicIp: process.env.PUBLIC_IP || "http://localhost:3000",
  port: process.env.PORT || 3030,
  host: process.env.MY_ADDRESS || "0.0.0.0",
  corsOrigin: process.env.CORS_ORIGIN || true,
};
