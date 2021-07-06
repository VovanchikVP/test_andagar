$(function () {
    var body = $('body');

    // Загрузка страницы.
    $(window).on('load', function (event) {
        add_date_page();
        add_curator_list();
    });

    // Отправка формы добавления факта из файла
    body.on('submit', '#form-add-xml-file', function (event) {
        event.preventDefault();
        $('div.load-block').show();
        let form = new FormData($(this)[0]);
        let url = '/api_v1/get_file/';
        post_form(form, url, $(this).attr('id'));
    });

    body.on('change', '#curator-select', function (event) {
        add_date_page();
    })
});

function add_date_page() {
    let list_data = get_list_labels();
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'line',
        data: {
        labels: list_data.label,
        datasets: [{
          label: 'График процедур',
          data: list_data.data,
          backgroundColor: "rgba(153,255,51,0.6)"
        }]
      }
    });
}

// Отправляет форму на сервер по средствам ajax
 function post_form(form, url, id_form){
    $.ajaxSetup({
         beforeSend: function(xhr, settings) {settings_ajax(xhr, settings)}
    });

    $.ajax({
        type: "POST",
        url: url,
        data: form,
        contentType: false,
        processData: false,
        success: function (data) {
            $('div.load-block').hide();
            if(data['status'] === 400){
                error_display(data);
            } else if(data['status'] === 200){
                location.reload()
            }
        },
        error: function (data) {
            error_post_ajax(data);
        }
    });
 }

function error_display(data) {
    $('#text-notific').text(data['heading']);
    $('#text-message').text(data['text']);
    $('#notification_modal').modal('show');
}

function error_post_ajax(data) {
    $('div.load-block').hide();
    $('#text-notific').text('Статус: ' + data.status + data.statusText);
    $('#notification_modal').modal('show');
}

function settings_ajax(xhr, settings) {
     if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
         xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
     }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function get_list_labels() {
    var select_curator = $('#curator-select').val();
    let label_list = [];
    let data_list = [];
    if (Object.keys(content.date).length){
        let sort_list_date = Object.keys(content.date).sort(function (a, b) {
            let date_a = new Date(a);
            let date_b = new Date(b);
            return date_a - date_b
        });

        if (+select_curator === 0){
            for(let i=0; i<sort_list_date.length; i++){
                label_list.push(sort_list_date[i]);
                let el = 0;
                for (let j=0; j<content.date[sort_list_date[i]].length;j++){
                    el += +content.data_all[content.date[sort_list_date[i]][j]].lot_max_price;
                }
                data_list.push(el)
            }
        } else {
            let pass_list = content.curator[select_curator];
            for(let i=0; i<sort_list_date.length; i++) {
                let el = 0;
                for (let j=0; j<content.date[sort_list_date[i]].length; j++) {
                    if (pass_list.indexOf(content.date[sort_list_date[i]][j]) !== -1) {
                        el += +content.data_all[content.date[sort_list_date[i]][j]].lot_max_price
                    }
                }
                if(el > 0){
                    data_list.push(el);
                    label_list.push(sort_list_date[i])
                }
            }
        }
    }

    return {'label': label_list, 'data': data_list}
}

function add_curator_list() {
    let select_object = $('#curator-select');
    for (let i in content.curator_name){
        if(i !== 'null'){
            select_object.append($('<option>', {value: i, text: content.curator_name[i]}))
        } else {
            select_object.append($('<option>', {value: i}).text('Без куратора'))
        }
    }
}
