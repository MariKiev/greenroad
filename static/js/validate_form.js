function validateForm(url_arg, form_selector) {
    $('body').on('submit', form_selector, function () {
        var $form = $(this);
        $form.find('button[type="submit"]').prop('disabled', true);
        $form.find('span.error').remove();
        $.ajax({
            url: url_arg,
            data: $form.serialize(),
            type: 'POST',
            dataType: 'json',
            success: function (response) {
                $form.find('button[type="submit"]').prop('disabled', false);
                if ($.isEmptyObject(response)) {
                    $('body').off('submit', form_selector);
                    $form.submit();
                } else {
                    $.each(response, function (field, errors) {
                        var field_selector = $('#' + field);
                        $.each(errors, function (i, error) {
                            field_selector.after('<span class="error">' + error + '</span>');
                        });
                    });
                }
            }
        });
        return false;
    });
}

// jQuery.fn.extend({
//     validateForm: function(url_arg, form_selector) {
//         $('body').on('submit', form_selector, function () {
//             var $form = $(this);
//             $form.find('button[type="submit"]').prop('disabled', true);
//             $form.find('span.error').remove();
//             $.ajax({
//                 url: url_arg,
//                 data: $form.serialize(),
//                 type: 'POST',
//                 dataType: 'json',
//                 success: function (response) {
//                     $form.find('button[type="submit"]').prop('disabled', false);
//                     if ($.isEmptyObject(response)) {
//                         $('body').off('submit', form_selector);
//                         $form.submit();
//                     } else {
//                         $.each(response, function (field, errors) {
//                             var field_selector = $('#' + field);
//                             $.each(errors, function (i, error) {
//                                 field_selector.after('<span class="error">' + error + '</span>');
//                             });
//                         });
//                     }
//                 }
//             });
//             return false;
//         });
//     }
// });

