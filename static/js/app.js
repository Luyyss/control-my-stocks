app = {'data':{}}

$(document).ready(function () {
    getData()
    getPrices()
    createGetDataInterval()
    getAutocompleteData()
})

function createGetDataInterval() {
    window.getDataInterval = setInterval(getPrices, 0.5 * 60 * 1000) // 1/2 minuto
}

function stopInterval() {
    clearInterval( window.getDataInterval )
}

function getData() {
    try {
        showLoader('#myAccordion')

        $.get('/app/data', function (data) {
            displayStocks(data)
            // displayLots(data.lots)
            // displayResumeTotal(data.info)
        })
    } catch (error) { console.log(error) }
}

function getPrices() {
    try {

        $.get('/app/prices', function (data) {
            displayStocksInfo(data.stocks)
            displayLots(data.lots)
            displayResumeTotal(data.info)
            if(! data.info.refresh ) 
                stopInterval()
        })
    } catch (error) { console.log(error) }
}

function getAutocompleteData() {
    try {
        $.get('/app/stocks', function (data) {
            autocomplete(document.getElementById("stock_name"), data );
        })
    } catch (error) { console.log(error) }
}

function displayStocksInfo(data) {
    for (let i = 0; i < data.length; i++) {
        info = data[i]

        $('#stock'+info['code']).find('.change').html(info['change'])
        $('#stock'+info['code']).find('.price').html(info['price'])
        $('#stock'+info['code']).find('.avg').html(info['avg_cost'])
        $('#stock'+info['code']).find('.stats').html(info['resume'])
    }
}

function displayStocks(data) {

    renderStocksTitle()

    for (let i = 0; i < data.length; i++) {
        renderStock( data[i], i )
    }
}

function renderStocksTitle() {
    $('#myAccordion').html(
        '<div class="card">\n\
            <div class="card-header" id="head" data-toggle="collapse" data-target="#collapse" aria-expanded="true" \n\
                aria-controls="collapse">\n\
                <div class="row">\n\
                    <div class="col-1">Código</div>\n\
                    <div class="col-2">Ações</div>\n\
                    <div class="col-2">Hoje</div>\n\
                    <div class="col-2">Preço</div>\n\
                    <div class="col-2">P. médio</div>\n\
                    <div class="col-2">Saldo</div>\n\
                    <div class="col-1">&nbsp;</div>\n\
                </div>\n\
            </div>\n\
        </div>'
    )
}

function displayLots(data) {
    for (let i = 0; i < data.length; i++) {
        renderLot( data[i] )
    }
}

function renderStock(stock, i) {
    $('#myAccordion').append('<div class="card" id="stock'+stock[0]+'">\n\
        <div class="card-header cursor" id="head' + i + '" data-toggle="collapse" data-target="#collapse' + i + '" aria-expanded="true" \n\
            aria-controls="collapse' + i + '">\n\
            <div class="row">\n\
                <div class="col-1">' + stock[0] + '</div>\n\
                <div class="col-2">' + stock[2] + '</div>\n\
                <div class="col-2 change"></div>\n\
                <div class="col-2 price"></div>\n\
                <div class="col-2 avg"></div>\n\
                <div class="col-2 stats"></div>\n\
                <div class="col-1"><img src="/static/image/x-square.svg" title="Remover ação" class="cursor" onclick="requestRemove(\''+stock[0]+'\')"/></div>\n\
            </div>\n\
        </div>\n\
        <div id="collapse' + i + '" class="collapse" aria-labelledby="head' + i + '" data-parent="#myAccordion">\n\
            <div class="card-body">\n\
                <div class="lots"></div>\n\
                <button type="button" class="btn white" onclick="requestAddLot(\''+stock[0]+'\')">\n\
                    <img src="/static/image/plus-square.svg"/>\n\
                </button>\n\
            </div>\n\
        </div>\n\
    </div>')
}

function displayResume(resume) {
    try{
        if (isNaN(parseFloat(resume[0])) )
            throw "empty";
        return displayMoney(resume[0]) + ' ( '+resume[1] + '% )'
    }
    catch(e) {
        return '----'
    }
}

function renderLot(lot) {
    $('#stock'+lot[1]+' .collapse .card-body .lots').append('<div class="lot" id="lot'+lot[0]+'">\n\
            <div class="row">\n\
                <div class="col-3">' + lot[4] + '</div>\n\
                <div class="col-3">' + lot[2] + '</div>\n\
                <div class="col-2">' + displayMoney(lot[3]) + '</div>\n\
                <div class="col-3">' + displayMoney(parseInt(lot[2]) * parseFloat(lot[3])) + '</div>\n\
                <div class="col-1"><img src="/static/image/x-square.svg" title="Remover ação" class="cursor" onclick="requestRemoveLot('+lot[0]+', \''+lot[1]+'\')"/></div>\n\
            </div>\n\
        </div>')
}

function displayMoney(m) {
    if(m == '0')
        return '----'
    return 'R$ '+parseFloat(m).toFixed(2)
}

function salvarNovaAcao() {

    stock_name = $('#stock_name').val();
    if (stock_name != '' && stock_name.includes(' | ')) {
        $.post('/app/stock', { 'stock': stock_name }, function (res) {

            $('#stock_name').val('')

            if(res.status == 'ok')
                getData()
        });
    }

    $('#exampleModal').modal('hide');
}

function requestRemove(stock) {
    event.stopPropagation()
    if(confirm('Deseja realmente remover esta ação?')) {
        $.ajax({
            url: '/app/stock',
            type: 'DELETE',
            data: {'stock':stock},
            success: function(res) {
                if(res.status == 'ok')
                    $('#stock'+stock).remove()
            }
        });
    }
}

function showLoader(target) {
    $(target).html('<div class="loader"><img src="/static/image/loader.svg"/></div>')
}

function requestAddLot(stock) {
    stopInterval()
    app.data.stock = stock
    $('#stock'+stock+' .card-body').append( getBlockAddLot() )

    IMask( document.getElementsByClassName('date-mask'),{
        mask: Date,
        // min: new Date(1990, 0, 1),
        // max: new Date(2020, 0, 1),
        lazy: false
    });

    IMask(document.getElementsByClassName('money-mask'), {
        mask: Number,
        thousandsSeparator: '.',
        scale: 2,
        radix: ',',
        min: 0
    });
}

function getBlockAddLot() {
    return '<form onsubmit="return saveNewLot(this)">\n\
                <div class="row">\n\
                    <div class="col-3">\n\
                        <label>Data</label>\n\
                        <input type="text" name="data" class="date-mask"/>\n\
                    </div>\n\
                    <div class="col-3">\n\
                        <label>Quantidade</label>\n\
                        <input type="number" name="qtd"/>\n\
                    </div>\n\
                    <div class="col-3">\n\
                        <label>Preço</label>\n\
                        <input type="text" name="preco" class="money-mask"/>\n\
                    </div>\n\
                    <div class="col-2 contentPaidValue">\n\
                        <b</b>\n\
                    </div>\n\
                    <div class="col-1">\n\
                        <button type="submit" onclick="saveAddLot(this)"><img src="static/image/check-square.svg"/></button>\n\
                    </div>\n\
                </div>\n\
            </form>'
}

function saveAddLot(el) {
    return saveNewLot( $(el).parent().parent().parent() )
}

app.isSalvando = false

function saveNewLot(el) {

    if( ! app.isSalvando) {

        app.isSalvando = true

        data = {
            'stock':app.data.stock,
            'data':$(el).find("input[name='data']").val(),
            'qtd':$(el).find("input[name='qtd']").val(),
            'preco':$(el).find("input[name='preco']").val()
        }

        if(data.qtd != '' && data.preco != '') {
            $.post('/app/lot', data, function(res) {

                app.isSalvando = false

                if(res.status == 'ok') {
                    getData()
                    createGetDataInterval()
                }
            })
        }
    }
    
    return false
}

function requestRemoveLot(id, stock) {
    event.stopPropagation()
    if(confirm('Deseja realmente remover este lote?')) {
        $.ajax({
            url: '/app/lot',
            type: 'DELETE',
            data: {'id':id, 'stock':stock},
            success: function(res) {
                console.log(res)
                $('#lot'+id).remove()
            }
        });
    }
}

function displayResumeTotal(data) {
    // {"result":98.46,"result_percent":7.23,"total_paid":1361.25996,"total_today":1459.72},
    $('#stocksResume').html(
        '<b>'+displayMoney(data['total_today'])+'</b>\n\
        <span>'+displayMoney(data['result'])+' ('+data['result_percent']+'%) </span>'
    )
}


function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function (e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
                salvarNovaAcao()
            }
        }
    });
    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }
    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}