const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const trackedProductsSchema = new Schema({
    url: {
        type: String,
        require: true,
    },
    price: {
        type: Number,
        require: true,
    },
    name: {
        type: String,
        require: true,
    },
    userPhone: {
        type: String,
        require: true,
    },
});

const Tracking = mongoose.model('trackedproducts', trackedProductsSchema);
module.exports = {
    Tracking
};