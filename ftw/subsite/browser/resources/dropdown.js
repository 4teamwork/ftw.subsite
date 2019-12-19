(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module. (Plone 5 with requirejs)
        define(['jquery'], factory);
    } else {
        // Browser globals (Plone 4 without requirejs)
        factory(root.jQuery);
    }
}(typeof self !== 'undefined' ? self : this, function ($) {
  function hideAllMenus() {
      $('dl.actionMenu').removeClass('activated').addClass('deactivated');
  }

  function toggleMenuHandler(event) {
      // swap between activated and deactivated
      $(this).parents('.actionMenu:first')
          .toggleClass('deactivated')
          .toggleClass('activated');
      return false;
  }

  function actionMenuDocumentMouseDown(event) {
      if ($(event.target).parents('.actionMenu:first').length) {
          // target is part of the menu, so just return and do the default
          return true;
      }

      hideAllMenus();
  }

  function actionMenuMouseOver(event) {
      var menu_id = $(this).parents('.actionMenu:first').attr('id'),
          switch_menu;
      if (!menu_id) {return true;}

      switch_menu = $('dl.actionMenu.activated').length > 0;
      $('dl.actionMenu').removeClass('activated').addClass('deactivated');
      if (switch_menu) {
          $('#' + menu_id).removeClass('deactivated').addClass('activated');
      }
  }

  function initializeMenus() {
      $(document).mousedown(actionMenuDocumentMouseDown);

      hideAllMenus();

      // add toggle function to header links
      $('dl.actionMenu dt.actionMenuHeader a')
          .click(toggleMenuHandler)
          .mouseover(actionMenuMouseOver);

      // add hide function to all links in the dropdown, so the dropdown closes
      // when any link is clicked
      $('dl.actionMenu > dd.actionMenuContent').click(hideAllMenus);
  }

  $(initializeMenus);
}));
