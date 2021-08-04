import express from "express";
import connectPython_associate from "../src/connectPython_associate";
import connectPython_find from "../src/connectPython_find";
import connectPython_get from "../src/connectPython_get";

const router = express.Router();

router.use("/echo", connectPython_associate);
router.use("/find", connectPython_find);
router.use("/get", connectPython_get);

export default router;
