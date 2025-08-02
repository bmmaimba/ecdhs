odoo.define('network_drives.network_path_widget', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
    var core = require('web.core');

    var NetworkPathWidget = AbstractField.extend({
        supportedFieldTypes: ['char'],
        events: {
            'click .copy-path-btn': '_onCopyPath',
        },

        _renderReadonly: function () {
            var value = this.value || '';
            var $container = $('<div>');
            $container.append($('<span>', { text: value, style: 'margin-right:8px;' }));
            $container.append($('<button>', {
                type: 'button',
                class: 'copy-path-btn',
                text: 'Copy',
                'data-path': value
            }));
            this.$el.html($container);
            return this._super.apply(this, arguments);
        },

        _onCopyPath: function (ev) {
            ev.preventDefault();
            var path = $(ev.currentTarget).data('path');
            navigator.clipboard.writeText(path).then(() => {
                this.displayNotification({
                    type: 'success',
                    title: 'Copied!',
                    message: path,
                    sticky: false,
                });
            }).catch(() => {
                this.displayNotification({
                    type: 'warning',
                    title: 'Copy failed',
                    message: 'Please copy manually: ' + path,
                    sticky: true,
                });
            });
        }
    });

    field_registry.add('network_path_widget', NetworkPathWidget);
    return NetworkPathWidget;
});