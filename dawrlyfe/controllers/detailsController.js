const fetch = require("node-fetch");


const getProduct = (req, res) => {
    const productCode = req.query.code;
    console.log(productCode);

    var requestOptions = {
        method: "GET",
        redirect: "follow",
    };

    const fetchAPI =  fetch(
            " https://2554-2c0f-fc89-80a6-cc29-c424-f3b0-7750-986.eu.ngrok.io/product/"+ productCode,
            requestOptions )
        .then(response => response.text())
        .then(result => {
            res.render('details', {
                reviews: result
            });
            /* res.send(result); */
        })
        .catch(error => console.log('error', error));
};

module.exports = {
    getProduct,
};