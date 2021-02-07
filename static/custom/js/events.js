var all_occurrences = new Set();
var all_roots = new Set();
var storage = window.localStorage;

const $corpus_table = $("#corpus_viewer");

const $form_prepare_entity = $("#form_prepare_entity");
const $line_id_entity = $("#line_id_entity");
const $entity_occurrence = $("#input_entity_occurrence");
const $entity_root = $("#input_entity_root");
const $entity_type = $("#input_entity_type");

const $add_entity_button = $("#add_entity");

const $confirm_entity_button = $("#confirm_entity_list");
const $entity_list = $("#entity_list");

const $form_prepare_relation = $("#form_prepare_relation");
const $line_id_relation = $("#line_id_relation");
const $relation_source = $("#input_relation_source");
const $relation_label = $("#input_relation_label");
const $relation_target = $("#input_relation_target");

const $add_relation_button = $("#add_relation")

const $confirm_relation_button = $("#confirm_relation_list");
const $relation_list = $("#relation_list");

const $datalist_occurrence = $("#datalist_occurrence");
const $datalist_root = $("#datalist_root");
const $datalist_source = $("#datalist_source");
const $datalist_target = $("#datalist_target");

$corpus_table.on('load-success.bs.table', function (e, data, status, xhr) {
    all_occurrences.clear();
    all_roots.clear();
    for (row of data) {
        for (entity of row.entity) {
            all_occurrences.add("<option>" + entity.occurrence + "</option>");
            all_roots.add("<option>" + entity.root + "</option>");
        }
    }
});

$corpus_table.on('check.bs.table', function (e, row, $element, field) {
    $corpus_table.bootstrapTable('collapseAllRows');
    $corpus_table.bootstrapTable('expandRow', $element.data('index'));
});

$corpus_table.on('expand-row.bs.table', function (e, index, row, $detail) {
    $line_id_entity.val(row.line_id);
    $line_id_relation.val(row.line_id);
    $entity_occurrence.val("");
    $entity_root.val("");
    $relation_source.val("");
    $relation_target.val("");

    var row_occurrences = new Set ();
    var row_roots = new Set();
    $.each(row.analysis, function(index, word) {
        if (word.is_noun) {
            row_occurrences.add("<option>" + word.original + "</option>");
            row_roots.add("<option>" + word.root + "</option>");
        }
    });

    var suggest_occurrences = new Set([...row_occurrences, ...all_occurrences]);
    var suggest_roots = new Set([...row_roots, ...all_roots]);

    $datalist_occurrence.html("");
    $datalist_occurrence.append(Array.from(suggest_occurrences).join(""));
    $datalist_root.html("");
    $datalist_root.append(Array.from(suggest_roots).join(""));

    $datalist_source.html("");
    $datalist_source.append(Array.from(suggest_roots).join(""));
    $datalist_target.html("");
    $datalist_target.append(Array.from(suggest_roots).join(""));

    var entity_list_html = [];
    var relation_list_html = [];

    $.each(row.entity, function (index, entity) {
        entity_html = entity_formatter(entity.occurrence, entity.root, entity.type);
        entity_list_html.push(entity_html);
    });

    $.each(row.relation, function (index, relation) {
        relation_html = relation_formatter(relation.source, relation.label, relation.target)
        relation_list_html.push(relation_html);
    });

    var unconfirmed = storage.getItem(row.line_id);
    var unconfirmed_relations = storage.getItem(row.line_id + '_relations');

    if (unconfirmed !== null) {
        $.each(JSON.parse(unconfirmed), function (index, entity) {
            entity_html = entity_formatter(entity.occurrence, entity.root, entity.type, "list-group-item-warning");
            entity_list_html.push(entity_html);
        });
    }
    if (unconfirmed_relations !== null) {
        $.each(JSON.parse(unconfirmed_relations), function (index, relation) {
            relation_html = relation_formatter(relation.source, relation.label, relation.target, "list-group-item-warning");
            relation_list_html.push(relation_html);
        });
    }
    $entity_list.html("").append(entity_list_html.join(""));
    $relation_list.html("").append(relation_list_html.join(""));
    $('[name="entity"]').bootstrapToggle();
    $('[name="relation"]').bootstrapToggle();
});

$corpus_table.on('page-change.bs.table', function (e, number, size) {
    $line_id_entity.val("");
    $line_id_relation.val("");
    $entity_occurrence.val("");
    $entity_root.val("");
    $relation_source.val("");
    $relation_target.val("");
    $relation_label.val("");
});
