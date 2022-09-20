console.log("Search js triggered");
var productName = JSON.parse(productName);

//console.log(productsList);

resultsNum = document.getElementById('resultsNum');

buildResults(productsList);

function buildResults(stores) {
    numberOfResults = 0;
    /* stores.forEach(store => {
        store.forEach(item => {
            numberOfResults++;
            addRow(item);
        });
    }); */
    largest = Math.max(stores[0].length, stores[1].length, stores[2].length);
    for (i = 0; i < largest; i++) {
        if (i < stores[0].length) {
            addRow(stores[0][i]);
            numberOfResults++;
        }
        if (i < stores[1].length) {
            addRow(stores[1][i]);
            numberOfResults++;
        }
        if (i < stores[2].length) {
            addRow(stores[2][i]);
            numberOfResults++;
        }
    }

    $(document).ready(function () {
        $("#pagination-container").append('<nav aria-label="Search Pagination"> <ul id="pagination" class="pagination"></ul> </nav>');
        var rowsShown = 10;
        var rowsTotal = numberOfResults;
        var numPages = rowsTotal / rowsShown;

        for (i = 0; i < numPages; i++) {
            var pageNum = i + 1;
            $("#pagination").append(
                '<li class="page-item"> <a class="page-link" href="#" rel="' + i + '">' + pageNum + "</a></li> "
            );
        }
        $("#searchResults #product").hide();
        $("#searchResults #product").slice(0, rowsShown).show();
        $("#pagination a:first").addClass("active");
        $("#pagination a").bind("click", function () {
            $("#pagination a").removeClass("active");
            $(this).addClass("active");
            var currPage = $(this).attr("rel");
            var startItem = currPage * rowsShown;
            var endItem = startItem + rowsShown;
            $("#searchResults #product")
                .css("opacity", "0.0")
                .hide()
                .slice(startItem, endItem)
                .css("display", "table-row")
                .animate({
                    opacity: 1,
                },
                    300
                );
        });
    });

    resultsNum.textContent = numberOfResults + " results for \"" + productName + "\"";
}

function addRow(product) {
    searchResults = $("#searchResults");

    var productRow = document.createElement("div");
    productRow.className = 'product';
    productRow.id = 'product';

    var productImage = document.createElement("div");
    productImage.className = 'product-image col-3';

    anchorTag = document.createElement("a");
    anchorTag.href = product["url"];
    imageTag = document.createElement("img");
    imageTag.src = product["image"];
    anchorTag.appendChild(imageTag);
    productImage.appendChild(anchorTag);

    var productDetails = document.createElement("div");
    productDetails.className = 'details col-6';

    var productName = document.createElement("div");
    formTag = document.createElement("form");
    formTag.action = "/product";
    formTag.type = "POST";

    inputTag = document.createElement("input");
    inputTag.name = "code";
    inputTag.value = product["code"];
    inputTag.type = "hidden";

    productName.className = 'product-name';
    headerTag = document.createElement("h2");
    buttonTag = document.createElement("button");
    buttonTag.textContent = product["name"];
    buttonTag.type = "submit";
    buttonTag.style = "float: left";
    buttonTag.addEventListener('click', () => {
        sessionStorage.product = JSON.stringify(product); 
    });

    formTag.append(buttonTag,inputTag);
    headerTag.appendChild(formTag);
    productName.appendChild(headerTag);

    var productPrice = document.createElement("div");
    productPrice.className = 'product-price';
    anchorTag = document.createElement("a");
    anchorTag.href = product["url"];
    anchorTag.textContent = "EGP " + product["price"];
    productPrice.appendChild(anchorTag);

    var trackProduct = document.createElement("div");
    trackProduct.className = 'track-product';
    buttonTag = document.createElement("button");
    buttonTag.id = "track";
    spanTag = document.createElement("span");
    spanTag.className = "material-icons";
    spanTag.style = "color:#71bf44";
    spanTag.textContent = "favorite_border";
    buttonTag.append(spanTag);

    spanTag.addEventListener('click', function handleClick() {
        $(this).text("favorite");
    });


    buttonTag.addEventListener('click', async _ => {
        try {
            const response = await fetch('/track-product', {
                method: 'post',
                headers: {
                    'content-type': 'application/json;charset=UTF-8',
                },
                body: JSON.stringify({
                    url: product["url"],
                    price: product["price"],
                    name: product["name"],
                    userPhone: "01122656138",
                })
            })
            console.log('Completed!', response);
        } catch (err) {
            console.error(`Error: ${err}`);
        }
    });

    trackProduct.appendChild(buttonTag);

    var productSeller = document.createElement("div");
    productSeller.className = 'seller-details col-3';

    sellerImage = document.createElement("div");
    sellerImage.className = 'seller-image';
    anchorTag = document.createElement("a");
    anchorTag.href = product["url"];
    imageTag = document.createElement("img");
    imageTag.src = "/images/" + product["seller"] + ".png";
    anchorTag.appendChild(imageTag);
    sellerImage.appendChild(anchorTag);



    goButton = document.createElement("div");
    goButton.className = "go-button";
    buttonTag = document.createElement("button");
    buttonTag.textContent = "Go To Store >";
    buttonTag.addEventListener('click', function handleClick() {
        location.href= product["url"];
    });
    goButton.appendChild(buttonTag);

    productSeller.append(sellerImage, goButton);
    productDetails.append(productName, productPrice, trackProduct);
    productRow.append(productImage, productDetails, productSeller);
    searchResults.append(productRow);
}