$(document).ready(function() {
    getData()
})

function getData() {
    try {
        $.get('/app/data', function(data) {
            displayStocks(data.stocks)
        })
    } catch (error) { console.log(error) }
}

function displayStocks(data) {
    for (let i = 0; i < data.length; i++) {
        stock = data[i];

        $('#myAccordion').append('<div class="card">\n\
            <div class="card-header" id="head' + i + '" data-toggle="collapse" data-target="#collapse' + i + '" aria-expanded="true" \n\
                aria-controls="collapse' + i + '">\n\
                <div class="row">\n\
                    <div class="col-4">' + stock.name + '</div>\n\
                    <div class="col-4">' + stock.price + '</div>\n\
                    <div class="col-4">' + stock.change + '</div>\n\
                </div>\n\
            </div>\n\
            <div id="collapse' + i + '" class="collapse" aria-labelledby="head' + i + '" data-parent="#myAccordion">\n\
                <div class="card-body">\n\
                    Content ' + stock.name + '\n\
                </div>\n\
            </div>\n\
        </div>')
    }
}

function requestAdd() {
    var stock = prompt('Insira o código da ação', "");

    if (stock != null) {
        alert(stock)
    }
}