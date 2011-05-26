jQuery(document).ready(function($) {
  $('.submit-row').closest('form').submit(function (e) {
    if ($('iframe').contents().find('input[name=_save]').size() != 0) {
      if (!confirm("Some plugins are still open and you have first to save them\nif you do not want to lose any changes you might made there.\nDo you still want to save?")) {
        e.preventDefault();
        return false;
      }
      else {
        return true;
      }
    }
  });
});
