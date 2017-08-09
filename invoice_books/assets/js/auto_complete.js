$(function () {

    // Autocomplete related functions

    function select2_util(elem, autocompleteURL) {
        elem.select2({
            ajax: {
                url: autocompleteURL,
                dataType: 'json',
                delay: 150,
                data: function (params) {
                    return params;
                },
                processResults: function (data, page) {
                    return {
                        results: data.results
                    };
                },
                cache: true
            },
            minimumInputLength: 1
        });
    }

    select2_util($('.js_item_select'), '/inventory/autocomplete/');
    select2_util($('.js_customer_select'), '/customer/autocomplete/');

});