odoo.define('housing_project_management.dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var HousingDashboard = AbstractAction.extend({
        template: 'housing_project_dashboard',

        start: function () {
            var self = this;
            return this._rpc({
                model: 'housing.project',
                method: 'get_dashboard_data',
                args: [],
            }).then(function (data) {
                self.$el.html(QWeb.render('housing_project_dashboard', {
                    widget: {
                        data: data
                    }
                }));
            });
        },
    });

    core.action_registry.add('housing_project_dashboard', HousingDashboard);
    return HousingDashboard;
});