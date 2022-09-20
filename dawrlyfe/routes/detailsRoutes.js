const express = require("express");
const detailsController = require('../controllers/detailsController');

const router = express();

router.get("/product", detailsController.getProduct);


module.exports = router;