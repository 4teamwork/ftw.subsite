!function(e,n){"function"==typeof define&&define.amd?define("subsite_dropdown",["jquery"],n):n(e.jQuery)}("undefined"!=typeof self?self:this,function(e){function n(){e('[id="portal-languageselector"]').removeClass("activated").addClass("deactivated")}function t(){return e(this).parents("#portal-languageselector").toggleClass("activated").toggleClass("deactivated"),!1}function a(t){0===e(t.target).parents("#portal-languageselector").length&&n()}function o(){n(),e(document).on("mousedown",a),e("#portal-languageselector .actionMenuHeader a").on("click",t),e("#portal-languageselector .actionMenuContent").on("click",n)}e(o)}),require(["subsite_dropdown"],function(e){}),define("main",function(){});