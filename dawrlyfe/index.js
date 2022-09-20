const express = require("express");
const app = express();
const port = 3000;
const mongoose = require('mongoose');

const searchRoutes = require('./routes/searchRoutes');
const detailsRoutes = require('./routes/detailsRoutes');

const bodyParser = require("body-parser");
/* const cors = require('cors'); */

mongoose.connect('mongodb+srv://adham:adhamDawrly1.@dawrlycluster.4m7b9.mongodb.net/DawrlyDB?retryWrites=true&w=majority');


app.use(
    bodyParser.urlencoded({
        extended: true,
    })
);
app.use(express.json());
app.use(express.static("public"));
/* app.use(cors()); */

app.set("view engine", "ejs");

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});

app.use(searchRoutes);
app.use(detailsRoutes);

app.get("/", (req, res) => {
    res.render("home");
});
app.get("/login", (req, res) => {
    res.render("user/login");
});
app.get("/register", (req, res) => {
    res.render("user/register");
});
app.get("/x", (req, res) => {
    res.render("details");
});
app.use((req, res) => {
    res.status(404).render("404");
});