(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module. (Plone 5 with requirejs)
        define(['jquery'], factory);
    } else {
        // Browser globals (Plone 4 without requirejs)
        factory(root.jQuery);
    }
}(typeof self !== 'undefined' ? self : this, function ($) {
  function hide() {
      $('#portal-languageselector').removeClass('activated').addClass('deactivated');
  }

  function toggle() {
      $('#portal-languageselector')
          .toggleClass('deactivated')
          .toggleClass('activated');
      return false;
  }

  function hideOnOutsideClick(event) {
      if ($(event.target).parents('#portal-languageselector').length === 0) {
          hide();
      }
  }

  function initializeMenu() {
      hide();

      $(document).on('mousedown', hideOnOutsideClick);

      $('#portal-languageselector .actionMenuHeader a').on('click', toggle)
      $('#portal-languageselector .actionMenuContent').on('click', hide);
  }

  $(initializeMenus);
}));
