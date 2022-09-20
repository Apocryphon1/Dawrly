const fetch = require("node-fetch");
const trackModel = require("../models/track");

const getProducts = (req, res) => {
    const productName = req.query.product;
    console.log(productName);
    var requestOptions = {
        method: "GET",
        redirect: "follow",
    };

    const fetchAPI =  fetch(
            " https://2554-2c0f-fc89-80a6-cc29-c424-f3b0-7750-986.eu.ngrok.io/" + productName,
            requestOptions )
        .then(response => response.text())
        .then(result => {
            //console.log(result);
            res.render('list', {
                allProducts: result, productName: productName
            });
        })
        .catch(error => console.log('error', error));
};

function addTrackedProduct(req, res) {
    console.log(req.body);
    const product = new trackModel.Tracking({
        url: req.body.url,
        price: req.body.price,
        name: req.body.name,
        userPhone: req.body.userPhone,
    });
    product
        .save()
        .then((result) => {
            console.log(result);
        })
        .catch((err) => {
            console.log(err);
        });
}

module.exports = {
    getProducts,
    addTrackedProduct,
};