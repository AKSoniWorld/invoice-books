$(function () {

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

    // Item-provision related functions

    function delete_item() {
        $(this).parents('.js_sub_form').fadeOut('fast');
        var deleted = $("input[id$='DELETE']:checked").length;
        var total = $("input[id$='DELETE']").length;
        console.log('total : ' + total);
        console.log('deleted : ' + deleted);
        var active = total - deleted - 1;
        if (active == 0) {
            $('#js_add_item').val('Add Items');
            $('#js_issue_item').hide();
        }
    }

    $("input[id$='DELETE']").change(delete_item);

    $("input[id$='DELETE']:checked").parents(".js_sub_form").hide();

    function cloneMore() {
        var newElement = $('#js_empty_sub_form').clone();
        var total = $('#id_form-TOTAL_FORMS').val();
        var div_id = newElement.attr('id').replace('empty', total);
        newElement.attr({'id': div_id});
        newElement.find('.select2-container').remove();
        newElement.html(newElement.html().replace(/__prefix__/g, total));
        select2_util(newElement.find('.js_item_select'), '/inventory/autocomplete/');
        select2_util(newElement.find('.js_customer_select'), '/customer/autocomplete/');
        newElement.find(".select2").attr({'style': 'width: 714px;'});
        newElement.find("input[id$='DELETE']").change(delete_item);
        newElement.show();
        total++;
        $('#id_form-TOTAL_FORMS').val(total);
        $('#js_sub_forms_table').append(newElement);
    }

    $('#js_add_item').click(function () {
        cloneMore();
        $('#js_add_item').val('Add More Items');
        $('#js_issue_item').show();
    });

});