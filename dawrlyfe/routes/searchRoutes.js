const express = require("express");
const searchController = require('../controllers/searchController');

const router = express();

router.get("/products", searchController.getProducts);
router.post("/track-product", searchController.addTrackedProduct);

module.exports = router;