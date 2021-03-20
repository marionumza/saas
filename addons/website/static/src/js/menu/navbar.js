harpiya.define('website.navbar', function (require) {
'use strict';

var core = require('web.core');
var dom = require('web.dom');
var publicWidget = require('web.public.widget');
var concurrency = require('web.concurrency');
var Widget = require('web.Widget');
var websiteRootData = require('website.root');

var qweb = core.qweb;

var websiteNavbarRegistry = new publicWidget.RootWidgetRegistry();

var WebsiteNavbar = publicWidget.RootWidget.extend({
    xmlDependencies: ['/website/static/src/xml/website.xml'],
    events: _.extend({}, publicWidget.RootWidget.prototype.events || {}, {
        'click [data-action]': '_onActionMenuClick',
        'mouseover > ul > li.dropdown:not(.show)': '_onMenuHovered',
        'click .o_mobile_menu_toggle': '_onMobileMenuToggleClick',
        'mouseover #oe_applications:not(:has(.dropdown-item))': '_onOeApplicationsHovered',
    }),
    custom_events: _.extend({}, publicWidget.RootWidget.prototype.custom_events || {}, {
        'action_demand': '_onActionDemand',
        'edit_mode': '_onEditMode',
        'readonly_mode': '_onReadonlyMode',
        'ready_to_save': '_onSave',
    }),

    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
        var self = this;
        var initPromise = new Promise(function (resolve) {
            self.resolveInit = resolve;
        });
        this._widgetDefs = [initPromise];
    },
    /**
     * @override
     */
    start: function () {
        var self = this;
        dom.initAutoMoreMenu(this.$('ul.o_menu_sections'), {
            maxWidth: function () {
                // The navbar contains different elements in community and
                // enterprise, so we check for both of them here only
                return self.$el.width()
                    - (self.$('.o_menu_systray').outerWidth(true) || 0)
                    - (self.$('ul#oe_applications').outerWidth(true) || 0)
                    - (self.$('.o_menu_toggle').outerWidth(true) || 0)
                    - (self.$('.o_menu_brand').outerWidth(true) || 0);
            },
        });
        return this._super.apply(this, arguments).then(function () {
            self.resolveInit();
        });
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _attachComponent: function () {
        var def = this._super.apply(this, arguments);
        this._widgetDefs.push(def);
        return def;
    },
    /**
     * As the WebsiteNavbar instance is designed to be unique, the associated
     * registry has been instantiated outside of the class and is simply
     * returned here.
     *
     * @override
     */
    _getRegistry: function () {
        return websiteNavbarRegistry;
    },
    /**
     * Searches for the automatic widget {@see RootWidget} which can handle that
     * action.
     *
     * @private
     * @param {string} actionName
     * @param {Array} params
     * @returns {Promise}
     */
    _handleAction: function (actionName, params, _i) {
        var self = this;
        return this._whenReadyForActions().then(function () {
            var defs = [];
            _.each(self._widgets, function (w) {
                if (!w.handleAction) {
                    return;
                }

                var def = w.handleAction(actionName, params);
                if (def !== null) {
                    defs.push(def);
                }
            });
            if (!defs.length) {
                // Handle the case where all action-capable components are not
                // instantiated yet (rare) -> retry some times to eventually abort
                if (_i > 50) {
                    console.warn(_.str.sprintf("Action '%s' was not able to be handled.", actionName));
                    return Promise.reject();
                }
                return concurrency.delay(100).then(function () {
                    return self._handleAction(actionName, params, (_i || 0) + 1);
                });
            }
            return Promise.all(defs).then(function (values) {
                if (values.length === 1) {
                    return values[0];
                }
                return values;
            });
        });
    },
    /**
     * @private
     */
    _whenReadyForActions: function () {
        return Promise.all(this._widgetDefs);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Called when the backend applications menu is hovered -> fetch the
     * available menus and insert it in DOM.
     *
     * @private
     * @param {Event} ev
     */
    _onOeApplicationsHovered: function (ev) {
        var self = this;
        this._rpc({
            model: 'ir.ui.menu',
            method: 'load_menus_root',
            args: [],
        }).then(function (result) {
            self.$('#oe_applications .dropdown-menu').html(
                $(qweb.render('website.oe_applications_menu', {menu_data: result}))
            );
        });
    },
    /**
     * Called when an action menu is clicked -> searches for the automatic
     * widget {@see RootWidget} which can handle that action.
     *
     * @private
     * @param {Event} ev
     */
    _onActionMenuClick: function (ev) {
        var $button = $(ev.currentTarget);
        $button.prop('disabled', true);
        var always = function () {
            $button.prop('disabled', false);
        };
        this._handleAction($button.data('action')).then(always).guardedCatch(always);
    },
    /**
     * Called when an action is asked to be executed from a child widget ->
     * searches for the automatic widget {@see RootWidget} which can handle
     * that action.
     */
    _onActionDemand: function (ev) {
        var def = this._handleAction(ev.data.actionName, ev.data.params);
        if (ev.data.onSuccess) {
            def.then(ev.data.onSuccess);
        }
        if (ev.data.onFailure) {
            def.guardedCatch(ev.data.onFailure);
        }
    },
    /**
     * Called in response to edit mode activation -> hides the navbar.
     *
     * @private
     */
    _onEditMode: function () {
        this.$el.addClass('editing_mode');
        this.do_hide();
    },
    /**
     * Called when a submenu is hovered -> automatically opens it if another
     * menu was already opened.
     *
     * @private
     * @param {Event} ev
     */
    _onMenuHovered: function (ev) {
        var $opened = this.$('> ul > li.dropdown.show');
        if ($opened.length) {
            $opened.find('.dropdown-toggle').dropdown('toggle');
            $(ev.currentTarget).find('.dropdown-toggle').dropdown('toggle');
        }
    },
    /**
     * Called when the mobile menu toggle button is click -> modifies the DOM
     * to open the mobile menu.
     *
     * @private
     */
    _onMobileMenuToggleClick: function () {
        this.$el.parent().toggleClass('o_mobile_menu_opened');
    },
    /**
     * Called in response to edit mode activation -> hides the navbar.
     *
     * @private
     */
    _onReadonlyMode: function () {
        this.$el.removeClass('editing_mode');
        this.do_show();
    },
    /**
     * Called in response to edit mode saving -> checks if action-capable
     * children have something to save.
     *
     * @private
     * @param {HarpiyaEvent} ev
     */
    _onSave: function (ev) {
        ev.data.defs.push(this._handleAction('on_save'));
    },
});

var WebsiteNavbarActionWidget = Widget.extend({
    /**
     * 'Action name' -> 'Handler name' object
     *
     * Any [data-action="x"] element inside the website navbar will
     * automatically trigger an action "x". This action can then be handled by
     * any `WebsiteNavbarActionWidget` instance if the action name "x" is
     * registered in this `actions` object.
     */
    actions: {},

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Checks if the widget can execute an action whose name is given, with the
     * given parameters. If it is the case, execute that action.
     *
     * @param {string} actionName
     * @param {Array} params
     * @returns {Promise|null} action's promise or null if no action was found
     */
    handleAction: function (actionName, params) {
        var action = this[this.actions[actionName]];
        if (action) {
            return Promise.resolve(action.apply(this, params || []));
        }
        return null;
    },
});

websiteRootData.websiteRootRegistry.add(WebsiteNavbar, '#oe_main_menu_navbar');

return {
    WebsiteNavbar: WebsiteNavbar,
    websiteNavbarRegistry: websiteNavbarRegistry,
    WebsiteNavbarActionWidget: WebsiteNavbarActionWidget,
};
});
