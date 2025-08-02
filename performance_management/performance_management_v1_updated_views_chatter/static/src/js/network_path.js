// static/src/js/network_path.js

odoo.define('network_path_viewer.network_path', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var core = require('web.core');
    var _t = core._t;

    ListController.include({
        _onButtonClick: function (event) {
            var record = this.model.get(event.data.record.id);
            if (event.data.attrs.name === 'action_open_path') {
                event.stopPropagation();
                var path = record.data.path.replace(/\\/g, '/');
                if (!path.startsWith('file:////')) {
                    path = 'file:////' + path.replace(/^\/+/, '');
                }
                window.open(path, '_blank');
                return;
            }
            return this._super.apply(this, arguments);
        },
    });
});