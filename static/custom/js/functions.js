function response_handler(response) {
    $('#corpus-title').html(response.title);
    return response.data;
}

function line_detail_formatter(index, row) {
    var words = [];
    var roots = [];
    var genders = [];
    var cases = [];
    var forms = [];
    var noun_markers = [];

    for (word of row.analysis) {
        words.push(word.original);
        roots.push(word.root);
        if (word.details !== {}) {
            genders.push(word.details.gender);
            cases.push(word.details.case);
            forms.push(word.details.form);
        } else {
            genders.push("");
            cases.push("");
            forms.push("");
        }
        noun_markers.push(word.is_noun);
    }

    var html = [
        '<div><table class="table table-responsive-sm table-striped">',
        '<tr><th scope="row">Word</th><td>' + words.join("</td><td>") + '</td></tr>',
        '<tr><th scope="row">Root</th><td>' + roots.join("</td><td>") + '</td></tr>',
        '<tr><th scope="row">Gender</th><td>' + genders.join("</td><td>") + '</td></tr>',
        '<tr><th scope="row">Case</th><td>' + cases.join("</td><td>") + '</td></tr>',
        '<tr><th scope="row">Number</th><td>' + forms.join("</td><td>") + '</td></tr>',
        '<tr><th scope="row">Noun?</th><td>' + noun_markers.join("</td><td>") + '</td></tr>',
        '</table></div>',
    ];

    return html.join("\n");
}

function column_marked_formatter(value, row) {
    return value ? '<i class="fa fa-check"></i>' : '';
}

function entity_formatter(occurrence, root, type, li_classes = "") {
    var entity_value = [occurrence, root, type].join('$');
    var li_class = 'list-group-item';
    if (li_classes !== "") {
        li_class += " " + li_classes;
    }
    var entity_html = [
        '<li class="' + li_class +'">',
        '<div class="row">',
        '<div class="col-sm-3">' + occurrence + '</div>',
        '<div class="col-sm-3 text-muted">' + root + '</div>',
        '<div class="col-sm-3 text-secondary">' + type + '</div>',
        '<div class="col-sm-3">',
        '<span class="float-right">',
        '<input type="checkbox" name="entity" value="' + entity_value + '" class="mr-5"',
        ' data-toggle="toggle" data-size="sm" data-on="<i class=\'fa fa-check\'></i>" ',
        ' data-off="<i class=\'fa fa-times\'></i>" data-onstyle="success"',
        ' data-offstyle="danger" checked>',
        '</span>',
        '</div>',
        '</div>',
        '</li>'
    ];
    return entity_html.join("");
}

function relation_formatter(source, label, target, li_classes = "") {
    var relation_value = [source, label, target].join('$');
    var li_class = 'list-group-item';
    if (li_classes !== "") {
        li_class += " " + li_classes;
    }
    var relation_html = [
        '<li class="' + li_class +'">',
        '<div class="row">',
        '<div class="col-sm">',
        '(' + source + ')',
        ' <span class="text-muted">⊢ [' + label + '] →</span> ',
        '(' + target + ')',
        '</div>',
        '<div class="col-sm-3">',
        '<span class="float-right">',
        '<input type="checkbox" name="relation" value="' + relation_value + '" class="mr-5"',
        ' data-toggle="toggle" data-size="sm" data-on="<i class=\'fa fa-check\'></i>" ',
        ' data-off="<i class=\'fa fa-times\'></i>" data-onstyle="success"',
        ' data-offstyle="danger" checked>',
        '</span>',
        '</div>',
        '</div>',
        '</li>'
    ];
    return relation_html.join("");
}

function row_attribute_handler(row, index) {
    return {}
}
