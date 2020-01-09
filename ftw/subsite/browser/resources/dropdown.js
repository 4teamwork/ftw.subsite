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
    $('[id="portal-languageselector"]').removeClass('activated').addClass('deactivated');
  }

  function toggle() {
    $(this).parents('#portal-languageselector').toggleClass('activated').toggleClass('deactivated');
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

  $(initializeMenu);
}));
