odoo.define('network_drives.network_path_open', function (require) {
    "use strict";

    var ListController = require('web.ListController');

    ListController.include({
        _onButtonClicked: function (event) {
            if (event.data.attrs.name === 'action_open_path') {
                var path = event.data.record.data.path;
                if (path) {
                    // Convert backslashes to slashes for file URI
                    var uri = 'file:///' + path.replace(/\\/g, '/');
                    window.open(uri, '_blank');
                }
            }
            this._super.apply(this, arguments);
        },
    });
});